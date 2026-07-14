import csv
import logging
import pickle
from pathlib import Path

import pandas as pd
import predefined_models
import xgboost
from rdkit import Chem
from rdkit.Chem import Descriptors, FilterCatalog
from rdkit.Chem.FilterCatalog import FilterCatalogParams

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()

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


def calculate_logS(molecules, models_dir: Path) -> list:
    """Takes in a list of RDKIT molecules and returns
    their LogS. Index of LogS = index in moleculeslist.

    Args:
        molecules: list of RDKIT molecules to find LogS of
        models_dir: where the models are held

    Returns:
        float: list of LogS for each molecule. Index in this list =
            molecule's index in molecules list
    """
    all_generated_descriptors = predefined_models.generate(molecules)

    # Import pretrained models
    mlp_model_import = pickle.load(open((models_dir / "aqsolpred_mlp_model.pkl"), "rb"))
    xgboost_model_import = pickle.load(
        open((models_dir / "aqsolpred_xgb_model.pkl"), "rb")
    )

    # predict test data (MLP,XGB,RF)
    pred_mlp = mlp_model_import.predict(all_generated_descriptors)
    pred_xgb = xgboost_model_import.predict(all_generated_descriptors)
    # calculate consensus
    pred_consensus = (pred_mlp + pred_xgb) / 2

    return pred_consensus


def rank_csv_in(csv_rank_file: Path) -> list:
    with open(csv_rank_file, "r") as f:
        return [line.strip().split(",") for line in f.read().strip().split("\n")]


def main(sdf_file: Path, csv_rank_file: Path, models_dir: Path, csv_file: Path):
    """Takes in an SDF file, calculates a number of statistics, and places into a csv file

    CSV file format:


    Args:
        sdf_file: the concat SDF file with all molecules
        csv_rank_file: CSV with all molecules listed in ranked order
            Index = index in sdf_file
        models_dir: Where LogP models are stored
        csv_file: csv file location
            Will create folder if it does not exist
    """
    # read in the molecules
    molecules = Chem.SDMolSupplier(
        str(sdf_file), sanitize=True, removeHs=False, strictParsing=True
    )
    # setup molecule analysis
    logs_list: list[float] = calculate_logS(molecules, models_dir)
    pains_catalog = build_pains_catalog()
    csv_rank_list: list[list] = rank_csv_in(csv_rank_file)
    # create csv
    data: list[list] = [
        [
            "SDF Index",
            "Name",
            "LogS",
            "CNN_VS",
            "CNNaffinity",
            "CNN_Score",
            "Group",
            "Molar Mass",
            "Heavy Atoms",
            "Lig Eff",
            "PAINS Flags",
            "SMILES",
            "Soluability",
            "Notes",
        ]
    ]
    for ind, mol in enumerate(molecules):
        temp_data: list = []
        # get SDF index
        temp_data.append(ind)
        # get name
        temp_data.append(mol.GetProp("_Name").strip())
        # get LogS of molecules
        temp_data.append(logs_list[ind])
        # Get CNN score
        cnn_vs: float = float(mol.GetProp("CNN_VS").strip())
        temp_data.append(cnn_vs)
        # get CNN Affinity
        cnn_affinity: float = float(mol.GetProp("CNNaffinity").strip())
        temp_data.append(cnn_affinity)
        # get CNN Score
        temp_data.append(cnn_vs / cnn_affinity)
        # get region/mol/group
        temp_data.append(
            f"{csv_rank_list[ind+1][1]}/{csv_rank_list[ind+1][2].split('.')[0]}"
        )
        # get molar mass
        temp_data.append(Descriptors.MolWt(mol))
        # get heavy atoms
        heavy_atoms: int = mol.GetNumHeavyAtoms()
        temp_data.append(heavy_atoms)
        # get lig eff
        temp_data.append(cnn_affinity / heavy_atoms)
        # get pains flags
        flags = [m.GetDescription() for m in pains_catalog.GetMatches(mol)]
        temp_data.append(";".join(flags) if flags else "")
        # get smiles
        temp_data.append(Chem.MolToSmiles(mol))
        # if soluable
        temp_data.append(
            "ok" if logs_list[ind] > -4.5 else "predicted to be poorly soluable"
        )
        # notes
        temp_data.append("")

        data.append(temp_data)

    if not csv_file.parent.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, "w", newline="") as f:
        csv.writer(f).writerows(data)


if __name__ == "__main__":
    # inputs
    sdf_file: Path = (
        DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs" / "overall_concat.sdf"
    ).resolve()
    csv_rank_file: Path = (
        DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs" / "overall_best.csv"
    ).resolve()
    models_dir: Path = DIR_SCRIPT / "models"
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "top_dock_stats.csv").resolve()
    main(sdf_file, csv_rank_file, models_dir, csv_file)
