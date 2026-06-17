from pathlib import Path
import csv
import MDAnalysis as mda
import json
from rdkit import Chem
from lib import *

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

PROLIF_TO_PHARMACOPHORE = {
    "Hydrophobic": "Hydrophobic",
    "HBDonor":     "HydrogenDonor",
    "HBAcceptor":  "HydrogenAcceptor",
    "PiStacking":  "Aromatic",
    "Cationic":    "PositiveIon",
    "Anionic":     "NegativeIon",
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
    residues: dict[str, list[str]] = {}
    """The protein residues interacting for each region"""
    inter_type: dict[str, list[str]] = {}
    """The type of interaction of those protein residues. Index aligns with above""" 
    if_interact: dict[str, list[list[str | list[int]]]] = {}
    """D1: region D2: each different molecule D3: each protein res interaction (index aligns above)
    D4: the ligand atoms it interacts with"""
    residues, inter_type, if_interact = read_in_csv(interaction_csv_dir)

    # read in the pharmacophores
    pharm_list: list[Path] = [item for item in pharm_json_dir.iterdir() if item.is_file() and item.suffix == ".json"]
    pharm_dict: dict[str, list] = {}
    """List of pharmacophores for each molecule in each region"""
    regions: list[str] = []
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)
        with open(pharm_json) as f:
            pharm_dict[region] = load_concatenated_json(pharm_json)
    
    # through each region and it's molecules
    for region_name, mol_list in pharm_dict.items():
        # read in the region
        region_file: Path = (docked_SDFs / f"{region_name}_concat.sdf").resolve()
        supplier = Chem.SDMolSupplier(str(region_file))
        for mol_index, mol_pharm in enumerate(mol_list):
            # extract molecule
            mol = supplier[mol_index]
            # determine if pharmacophore is valid
            reg_res_list: list[str] = residues[region_name]
            reg_inter_type: list[str] = inter_type[region_name]
            mol_if_interact: list[str | list] = if_interact[region_name][mol_index]
            valid_pharms: list[bool] = get_valid_pharms(mol_pharm, mol, reg_res_list, 
                                                        reg_inter_type, mol_if_interact)
            # update pharmacophore based on validity
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


def get_valid_pharms(mol_pharm, mol, res_list: list[str], 
                     inter_type_list: list[str], if_interact_list: list[str | list[int]]) -> list[bool]:
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
        if_any_inside: bool = False
        for res_index, res_name in enumerate(res_list):
            # if interacting in this molecule + correct type
            atoms_interact = if_interact_list[res_index]
            prolif_inter_type = PROLIF_TO_PHARMACOPHORE[inter_type_list[res_index]]
            if atoms_interact != "False" and pharm_type == prolif_inter_type:
                # go through each atom
                for atom in atoms_interact:
                    conf = mol.GetConformer()
                    atom_pos = list(conf.GetAtomPosition(atom))
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
        if dist < 1.7:
            return True
    if inter_type == "HydrogenDonor" or inter_type == "HydrogenAcceptor":
        if dist < 1.7:
            return True 
    if inter_type == "Cationic" or inter_type == "Anionic":
        if dist < 1.7:
            return True 
    return False







if __name__ == "__main__":
    # inputs
    interaction_csv_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data")
    protein_dir: Path = (DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb")
    docked_SDFs: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs")
    pharm_list: Path = (DIR_STUDY / "028-pharms-top-div-set" / "data")
    op_dir: Path = (DIR_SCRIPT / ".." / "data" / "imp_pharms")

    main(interaction_csv_dir, protein_dir, docked_SDFs, pharm_list, op_dir)


