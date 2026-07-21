import csv
import json
import logging
from pathlib import Path

from rdkit import Chem


PROLIF_TO_PHARMACOPHORE: dict[str,str] = {
    "Hydrophobic": "Hydrophobic",
    "HBDonor": "HydrogenDonor",
    "HBAcceptor": "HydrogenAcceptor",
    "PiStacking": "Aromatic",
    "Cationic": "PositiveIon",
    "Anionic": "NegativeIon",
}

from FapC_VS import enable_logging



def main(
    sdf_path: Path,
    csv_path: Path,
    pharm_json_path: Path,
    op_pharm_dir: Path,
    op_csv_path: Path,
    FILE_LOG: Path,
):
    """ALL IN CONTEXT OF A SINGLE CONCATED SDF FILE. Requires running of pharmit on that
    and interaction determination script on it.

    Will take in concated SDF, a csv that lists each molecules interactions (in that sdf), and
    concat json that lists each molecules pharmacophores (in that sdf). The indexing of each molecule
    should be same in each (1st in sdf = 1st of pharm = 1st in csv)

    With that, will determine which pharmacophores to disable and enable. Stores csv of which pharms are
    enable / disable for each molecule (index in csv = index in sdf = etc). Also exports all updated
    pharmacophore lists, though each molecule has a seperate file

    Args:
        sdf_path: where sdf with molecules is stored
        csv_path: where the csv of molecular interactions are stored
        pharm_json_path: where concat json with all pharmacophores are stored
        op_pharm_dir: where the updated jsons, 1 for each molecule, will be stored
            Note: no longer concat, each molecule has a seperate file
            Index of file = index of molecule in sdf
            Creates directory path if DNE
        op_csv_path: where the csv holding which pharms are enabled / disabled is stored
            Index in csv = index of molecule in sdf
            Creates directory path if DNE
    """
    # set up logging
    enable_logging(FILE_LOG)

    # read in the csv
    logging.info("Reading in csv...")
    residues: list[str] = []
    """The protein residues interacting"""
    inter_type: list[str] = []
    """The type of interaction of those protein residues. Index aligns with above"""
    if_interact: list[list[str | list[int]]] = []
    """D1: each different molecule D2: each protein res interaction (index aligns above)"""
    residues, inter_type, if_interact = read_in_csv(csv_path)

    # read in the pharmacophores concat json
    logging.info("Reading in pharmacophores...")
    pharm_list: list[dict] = []
    """List of pharmacophores for each molecule"""
    pharm_list = load_in_pharm_json(pharm_json_path)

    # modify pharmacophores
    logging.info("Modifying pharmacophores...")
    supplier = Chem.SDMolSupplier(
        str(sdf_path), sanitize=True, removeHs=False, strictParsing=True
    )
    new_pharm: list[dict] = []
    """New pharmacophores JSON for each molecule"""
    pharms_enable_list: list[list[bool]] = []
    """If pharms are enabled / disabled for each molecule"""
    for mol_index, pharm in enumerate(pharm_list):
        valid_pharms: list[bool] = get_valid_pharms(
            pharm, supplier[mol_index], residues, inter_type, if_interact[mol_index]
        )
        pharms_enable_list.append(valid_pharms)
        """Boolean list, if a pharmacophore is valid or not"""
        log_pharms(mol_index, valid_pharms)
        new_pharm.append(update_pharm(pharm, valid_pharms))

    # write out the new pharmacophores
    logging.info("Writing pharmacophores...")
    if not op_pharm_dir.is_dir():
        op_pharm_dir.mkdir(parents=True, exist_ok=True)
    for ind, pharm in enumerate(new_pharm):
        op_pharm_file: Path = op_pharm_dir / f"mol{ind}_input.json"
        with open(op_pharm_file, "w") as f:
            json.dump(pharm, f, indent=2)

    # write out csv of disale / enabled pharms
    logging.info("Writing csv...")
    if not op_csv_path.parent.is_dir():
        op_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(op_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(pharms_enable_list)

    logging.info(f"Completed\n")


def log_pharms(mol_index: int, valid_pharms: list[bool]):
    bool_count = valid_pharms.count(True)
    if bool_count > 3:
        logging.info(f"Mol{mol_index} has {bool_count} pharms")
    else:
        logging.warning(f"Mol{mol_index} has {bool_count} pharms. Check manually")


def update_pharm(mol_pharm: dict, valid_pharms: list[bool]) -> dict:
    """Will update the the pharm JSONs so that are enabled / disabled based
    on valid pharm list

    Args:
        mol_pharm: list of all pharms for this mol
        valid_pharms: which pharms should be enabled / disabled

    Returns:
        dict: pharms now enabled / disabled correctly
    """

    for index in range(len(mol_pharm["points"])):
        if not valid_pharms[index]:
            mol_pharm["points"][index]["enabled"] = False

    return mol_pharm


def get_valid_pharms(
    mol_pharm: dict,
    mol,
    res_list: list[str],
    inter_type_list: list[str],
    if_interact_list: list[str | list[int]],
) -> list[bool]:
    """For a single molecule, takes in it's pharmacophore JSON and compares it to present
    interactions. If the pharmacophore is close to interacting atoms (of the same type), enable it.
    Else disable it

    Args:
        mol_pharm: list of pharmacophores for molecule
        mol: the molecule being locked at
        res_list: list of all interaction residues for this molecule
            This + other 2 taken from interaction csv that includes this molecule
            Indicies should line up
        inter_type_list: type of finteraction for each residue
        if_interact_list: if that interaciton is happening

    Returns:
        list[bool]: list of pharmacophores for this molecule that are valid
    """
    if_pharm: list[bool] = []
    for pharm in mol_pharm["points"]:
        # get data about pharmacophore
        pharm_loc = [pharm["x"], pharm["y"], pharm["z"]]
        # for the full refactor we should workshop how to make this more efficient 
        # (use a numpy array to store all the data and work on it directly)
        pharm_type = pharm["name"]
        # go through each interacting residue
        if_any_inside: bool = False
        for res_index, res_name in enumerate(res_list):
            # if interacting in this molecule + correct type
            atoms_interact = if_interact_list[res_index]
            prolif_inter_type = PROLIF_TO_PHARMACOPHORE[inter_type_list[res_index]]
            if atoms_interact != "False" and pharm_type == prolif_inter_type:
                # go through each atom
                for atom in atoms_interact:
                    conf = mol.GetConformer()
                    atom_pos = list(conf.GetAtomPosition(int(atom) - 1))
                    # determine distance and if valid
                    dist: float = eucl_dist(atom_pos, pharm_loc)
                    if_any_inside = if_inside_pharm(dist, prolif_inter_type)
                    if if_any_inside:
                        break
            if if_any_inside:
                break
        if if_any_inside:
            if_pharm.append(True)
        else:
            if_pharm.append(False)

    return if_pharm


def if_inside_pharm(dist: float, inter_type: str) -> bool:
    if inter_type == "Hydrophobic" or inter_type == "Aromatic":
        if dist < 2:
            return True
    if inter_type == "HydrogenDonor" or inter_type == "HydrogenAcceptor":
        if dist < 2:
            return True
    if inter_type == "Cationic" or inter_type == "Anionic":
        if dist < 2:
            return True
    return False


def eucl_dist(a: list[int], b: list[int]) -> int:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def read_in_csv(
    inter_csv: Path,
) -> tuple[list[str], list[str], list[list[str | list[int]]]]:
    """Will take in a interaction list csv file and return lists describing each interaction.
    Each interaction has a specific index.

    Args:
        inter_csv: the path to the interaction csv

    Returns:
        residues: list of protein residues interaction
        inter_type: the type of interaction
        if_inter: if that interaction type is occuring for this molecule.
            No = False
            Yes = list of ligand atom indicies involved. Starts indexing at 1.
    """
    # read in interaction_csv_dir
    with open(inter_csv, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        residues = next(reader)
        inter_type = next(reader)
        if_interact = [
            [[int(u) for u in v.split(".")] if v != "False" else "False" for v in row]
            for row in list(reader)
        ]

    return residues, inter_type, if_interact


def to_bool(s):
    return s.strip().lower() in ("true", "1", "t", "yes")


def load_in_pharm_json(path: Path) -> list[dict]:
    """Takes in the concated pharmacophore file, and returns
    each seperate pharmacophore description in a list.
    The pharmacophore info itself is a dictionary

    Args:
        path: location of pharmacophore file

    Returns:
        A list of all pharmacophores stored in the file.
        The JSON of the pharmacophore is in dictionary format.
    """
    return load_concatenated_json(path)


def load_concatenated_json(path: Path) -> list[dict]:
    """Will take in a concatanated JSON file (basically multiple JSONs in one)
    and return a list of JSON objects for each one

    Args:
        path: location of json

    Returns:
        list: list of the jsons in the file
    """
    with open(path) as f:
        text = f.read()

    decoder = json.JSONDecoder()
    objects = []
    idx = 0
    n = len(text)
    while idx < n:
        while idx < n and text[idx].isspace():
            idx += 1
        if idx >= n:
            break
        obj, end = decoder.raw_decode(text, idx)
        objects.append(obj)
        idx = end
    return objects


def write_concatenated_json(objects, path, indent=2):
    with open(path, "w") as f:
        for i, obj in enumerate(objects):
            if i:
                f.write("\n")
            json.dump(obj, f, indent=indent)
