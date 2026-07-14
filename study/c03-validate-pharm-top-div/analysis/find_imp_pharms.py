from pathlib import Path
import csv
import json
from rdkit import Chem
from lib import *
import logging

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = (DIR_SCRIPT  / ".." / "..").resolve()
FILE_LOG: Path = (DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log").resolve()

def make_log_dir(file_log: Path = FILE_LOG):
    if not file_log.parent.is_dir():
        file_log.parent.mkdir(parents=True, exist_ok=True)

PROLIF_TO_PHARMACOPHORE = {
    "Hydrophobic": "Hydrophobic",
    "HBDonor":     "HydrogenDonor",
    "HBAcceptor":  "HydrogenAcceptor",
    "PiStacking":  "Aromatic",
    "Cationic":    "PositiveIon",
    "Anionic":     "NegativeIon",
}





def main(sdf_path: Path, csv_path: Path, pharm_json_path: Path, op_pharm_dir: Path, op_csv_path: Path, file_log: Path = FILE_LOG):
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
    make_log_dir(file_log)
    logging.basicConfig(
        filename=file_log,
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

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
    supplier = Chem.SDMolSupplier(str(sdf_path), sanitize=True, removeHs=False,
                                strictParsing=True)
    new_pharm: list[dict] = []
    """New pharmacophores JSON for each molecule"""
    pharms_enable_list: list[list[bool]] = []
    """If pharms are enabled / disabled for each molecule"""
    for mol_index, pharm in enumerate(pharm_list):
        valid_pharms: list[bool] = get_valid_pharms(pharm, supplier[mol_index], residues, 
                                                    inter_type, if_interact[mol_index])
        pharms_enable_list.append(valid_pharms)
        """Boolean list, if a pharmacophore is valid or not"""
        log_pharms(mol_index, valid_pharms)
        new_pharm.append(update_pharm(pharm, valid_pharms))

    # write out the new pharmacophores
    logging.info("Writing pharmacophores...")
    if not op_pharm_dir.is_dir():
        op_pharm_dir.mkdir(parents=True, exist_ok=True)
    for ind, pharm in enumerate(new_pharm):
        op_pharm_file: Path = (op_pharm_dir / f"mol{ind}_input.json")
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


if __name__ == "__main__":
    # base files
    interaction_csv_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data").resolve()
    docked_sdfs: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs").resolve()
    pharm_json_dir: Path = (DIR_STUDY / "028-pharms-top-div-set" / "data").resolve()
    op_dir: Path = (DIR_SCRIPT / ".." / "data").resolve()

    # extract regions
    regions: list[str] = []
    pharm_list: list[Path] = [item for item in pharm_json_dir.iterdir() if item.is_file() and item.suffix == ".json"]
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)
    
    # for each region
    for region in regions:
        sdf_path: Path = (docked_sdfs / f"{region}_concat.sdf").resolve()
        csv_path: Path = (interaction_csv_dir / f"{region}_interacts.csv").resolve()
        pharm_json_path: Path = (pharm_json_dir / f"{region}_concat.json").resolve()
        op_pharm_dir: Path = (op_dir / "script_output" / region).resolve()
        op_csv_path: Path = (op_dir / "pharm_enabled" / f"{region}.csv").resolve()
        
        main(sdf_path, csv_path, pharm_json_path, op_pharm_dir, op_csv_path)

