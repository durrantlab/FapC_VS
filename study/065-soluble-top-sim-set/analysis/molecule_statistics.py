from pathlib import Path
import logging
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import FilterCatalog
from rdkit.Chem.FilterCatalog import FilterCatalogParams
import csv
import pickle
import pandas as pd
import xgboost

import predefined_models

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()
FILE_LOG: Path = (DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log").resolve()

if not FILE_LOG.parent.is_dir():
    FILE_LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=FILE_LOG,
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)




def build_pains_catalog():
    params = FilterCatalogParams()
    params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
    return FilterCatalog.FilterCatalog(params)



def calculate_logS(molecules, models_dir: Path) -> list[float]:
    """Takes in an RDKIT molecule and returns
    its LogS

    Args:
        mol: an RDKIT molecule to find LogS of
        models_dir (Path): where the models are held

    Returns:
        float: the LogS of that molecule
    """
    all_generated_descriptors = [predefined_models.generate(mol) for mol in molecules]

    # Import pretrained models
    mlp_model_import = pickle.load(open((models_dir / "aqsolpred_mlp_model.pkl"), "rb"))
    xgboost_model_import = pickle.load(open((models_dir / "aqsolpred_xgb_model.pkl"), "rb"))

    # predict test data (MLP,XGB,RF)
    pred_mlp = mlp_model_import.predict(all_generated_descriptors)
    pred_xgb = xgboost_model_import.predict(all_generated_descriptors)
    # calculate consensus
    pred_consensus = (pred_mlp + pred_xgb) / 2

    return pred_consensus




def main(sdf_file: Path, models_dir: Path, csv_file: Path):
    """Takes in an SDF file, calculates a number of statistics, and places into a csv file

    CSV file format:


    Args:
        sdf_file (Path): the concat SDF file with all molecules
        models_dir (Path): Where LogP models are stored
        csv_file (Path): csv file location
            Will create folder if it does not exist
    """
    # read in the molecules
    molecules = Chem.SDMolSupplier(str(sdf_file), sanitize=True, removeHs=False,
                            strictParsing=True)
    # calculate LogS
    logs_list: list[float] = calculate_logS(molecules, models_dir)
    pains_catalog = build_pains_catalog()
    data: list[list] = [["Name","LogS","Molar Mass","Heavy Atoms","PAINS Flags","SMILES"]]
    for ind, mol in enumerate(molecules):
        temp_data: list = []
        # get name
        temp_data.append(mol.GetProp("_Name").strip())
        # get LogS of molecules
        temp_data.append(logs_list[ind])
        # Get CNN score
        # get CNN Affinity
        # get region/mol/group
        # get molar mass
        temp_data.append(Descriptors.MolWt(mol))
        # get heavy atoms
        temp_data.append(mol.GetNumHeavyAtoms())
        # get pains flags
        flags = [m.GetDescription() for m in pains_catalog.GetMatches(mol)]
        temp_data.append(";".join(flags) if flags else "")
        # get smiles
        temp_data.append(Chem.MolToSmiles(mol))

        data.append(temp_data)
    
    if not csv_file.parent.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, "w", newline="") as f:
        csv.writer(f).writerows(data)


if __name__ == "__main__":
    # inputs
    sdf_file: Path = (DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs" / "overall_concat.sdf").resolve()
    models_dir: Path = (DIR_SCRIPT / "models")
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "solubility.csv").resolve()
    main(sdf_file,models_dir,csv_file)


