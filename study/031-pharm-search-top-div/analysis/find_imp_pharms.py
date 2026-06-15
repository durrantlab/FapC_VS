from pathlib import Path
import csv
import MDAnalysis as mda
import json


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


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
    regions: list[str] = 
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)
        with open(pharm_json) as f:
            pharm_dict[region] = load_concatenated_json(pharm_json)
    
    # through each region and molecules
    for region_name, pharm_list in pharm_dict.items():
        for mol_index, mol_pharm in enumerate(pharm_list):
            # take the location of pharmacophore and check if it close enough to one of the
            # molecules with same type of interaction
        




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


