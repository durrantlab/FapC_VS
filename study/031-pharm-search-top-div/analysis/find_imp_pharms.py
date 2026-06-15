from pathlib import Path
import csv
import MDAnalysis as mda
import json

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

PROLIF_TO_PHARMACOPHORE = {
    "Hydrophobic": "Hydrophobic",
    "HBDonor":     "HydrogenAcceptor",
    "HBAcceptor":  "HydrogenDonor",
    "PiStacking":  "Aromatic",
    "Cationic":    "NegativeIon",
    "Anionic":     "PositiveIon",
    "VdWContact":  None,            
}

def main(interaction_csv_dir: Path, protein_dir: Path, 
         docked_SDFs: Path, pharm_json_dir: Path, op_dir: Path):
    """Will take in pharmacophores for each sdf and its
    list of interactions to determine key pharmacophores

    Args:
        interaction_csv_dir (Path): each molecules interactions
        protein_dir (Path): the protonated protein they were docked
        docked_SDFs (Path): the top molecules
        pharm_list (Path): list of the molecules pharmacophores
        op_dir (Path): where info on each molecule will be output
    """

    # read in interaction_csv_dir
    residues, inter_type, if_interact = read_in_csv(interaction_csv_dir)

    # read in the protein
    u = mda.Universe(protein_dir)

    # read in the pharmacophores
    pharm_list: list[Path] = [item for item in pharm_json_dir.iterdir() if item.is_file() and item.suffix == ".json"]
    pharm_dict: dict = {}
    regions: list[str] = []
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)
        with open(pharm_json) as f:
            pharm_dict[region] = load_concatenated_json(pharm_json)
    
    # through each region and it's molecules
    for region_name, pharm_list in pharm_dict.items():
        for mol_index, mol_pharm in enumerate(pharm_list):
            # take the location of pharmacophore and check if it close enough to one of the
            # molecules with same type of interaction
            reg_res_list: list[str] = residues[region_name]
            reg_inter_type: list[str] = inter_type[region_name]
            mol_if_interact: list[bool] = residues[region_name][mol_index]
            valid_pharms: list[bool] = get_valid_pharms(mol_pharm, u, reg_res_list, 
                                                        reg_inter_type, mol_if_interact)
            mol_pharm = update_pharm(mol_pharm, valid_pharms)

def update_pharm(mol_pharm: list, valid_pharms: list[bool]) -> list:
    """Will update the the pharm JSONs so that are enabled / disabled based
    on valid pharm list

    Args:
        mol_pharm (list[json]): list of all pharms for this mol
        valid_pharms (list[bool]): which pharms should be enabled / disabled

    Returns:
        list[json]: pharms now enabled / disabled correctly
    """

    for index in range(len(mol_pharm)):
        if not valid_pharms[index]:
            mol_pharm[index]["enabled"] = False
    
    return mol_pharm


def get_valid_pharms(mol_pharm: json, u: mda.Universe, res_list: list[str], 
                     inter_type_list: list[str], if_interact_list: list[bool]) -> list[bool]:
    """take the location of pharmacophore and check if it close enough to one of the
    molecules with same type of interaction. If it is, adds its index to the return
    list

    Args:
        mol_pharm (json): list of pharmacophores for molecule
        u (Universe): protein
        res_list (list[str]): list of all interaction residues in this region
        inter_type_list (list[str]): type o finteraction for each residue
        if_interact_list (list[bool]): if that interaciton is happening

    Returns:
        list[int]: list of pharmacophores for this molecule that are valid
    """
    if_pharm: list[bool] = []
    for pharm in mol_pharm["points"]:
        # get data about pharmacophore
        pharm_loc = [pharm["x"],pharm["y"],pharm["z"]]
        pharm_type = pharm["name"]
        # go through each interacting residue
        brk = False
        for res_ind, res in enumerate(res_list):
            # check that this res is involved in correct interacion type
            inter_type = PROLIF_TO_PHARMACOPHORE[inter_type_list[res_ind]]
            if inter_type == pharm_type:
                # get every atom and go through and find distance to pharm
                res_num = int(res.split(".")[0][3:])
                chain_id = res.split(".")[1]
                res_atoms_coords = u.select_atoms(f"resid {res_num} and chainID {chain_id}").positions
                for res_pos in res_atoms_coords:
                    dist = eucl_dist(res_pos, pharm_loc)
                    if if_interacting(dist, inter_type):
                        brk = True 
                        if_pharm.append(True)
                        break
            if brk:
                break
        if not brk:
            if_pharm.append(False)
    return if_pharm



def if_interacting(dist, inter_type) -> bool:
    if inter_type == "Hydrophobic" or inter_type == "Aromatic":
        if dist < 7:
            return True
    if inter_type == "HydrogenDonor" or inter_type == "HydrogenAcceptor":
        if dist < 4:
            return True 
    if inter_type == "HydrogenDonor" or inter_type == "HydrogenAcceptor":
        if dist < 4:
            return True 
    return False



def eucl_dist(a: list[int], b: list[int]) -> int:
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5



def read_in_csv(interaction_csv_dir: Path):
    # read in interaction_csv_dir
    inter_csv_list: list[Path] = [item for item in interaction_csv_dir.iterdir() if item.is_file() and item.suffix == ".csv"]

    residues: dict[list[str]] = {}
    inter_type: dict[list[str]] = {}
    if_interact: dict[list[list[str]]] = {}
    for inter_csv in inter_csv_list:
        region: str = "_".join(inter_csv.name.split(".")[0].split("_")[0:2])
        with open(inter_csv, newline="") as f:
            reader = csv.reader(f)
            next(reader)
            residues[region] = next(reader)
            inter_type[region] = next(reader)
            if_interact[region] = \
                [[to_bool(v) for v in row] for row in list(reader)]
    
    return residues, inter_type, if_interact



def to_bool(s):
    return s.strip().lower() in ("true", "1", "t", "yes")



def load_concatenated_json(path: Path) -> list:
    """Will take in a concatanated JSON file (basically multiple JSONs in one)
    and return a list of JSON objects for each one

    Args:
        path (_type_): location of json

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



if __name__ == "__main__":
    # inputs
    interaction_csv_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data")
    protein_dir: Path = (DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb")
    docked_SDFs: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs")
    pharm_list: Path = (DIR_STUDY / "028-pharms-top-div-set" / "data")
    op_dir: Path = (DIR_SCRIPT / ".." / "data" / "imp_pharms")

    main(interaction_csv_dir, protein_dir, docked_SDFs, pharm_list, op_dir)


