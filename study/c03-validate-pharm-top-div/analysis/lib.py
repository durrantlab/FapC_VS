from pathlib import Path
import csv
import json

PROLIF_TO_PHARMACOPHORE = {
    "Hydrophobic": "Hydrophobic",
    "HBDonor":     "HydrogenDonor",
    "HBAcceptor":  "HydrogenAcceptor",
    "PiStacking":  "Aromatic",
    "Cationic":    "PositiveIon",
    "Anionic":     "NegativeIon",
}






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





def get_valid_pharms(mol_pharm: dict, mol, res_list: list[str], 
                     inter_type_list: list[str], if_interact_list: list[str | list[int]]) -> list[bool]:
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
        pharm_loc = [pharm["x"],pharm["y"],pharm["z"]]
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
                    atom_pos = list(conf.GetAtomPosition(int(atom)-1))
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

def if_inside_pharm(dist, inter_type) -> bool:
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
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5



def read_in_csv(inter_csv: Path) -> tuple[list[str], list[str], list[list[str | list[int]]]]:
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
        if_interact = \
            [[[int(u) for u in v.split(".")] if v != "False" else "False" for v in row] for row in list(reader)]
    
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
