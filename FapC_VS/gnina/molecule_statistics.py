
import csv
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Descriptors, FilterCatalog
from rdkit.Chem.FilterCatalog import FilterCatalogParams
from aqsolpred_web.predict.predict_from_mol import calculate_logs

def build_pains_catalog():
    params = FilterCatalogParams()
    params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
    return FilterCatalog.FilterCatalog(params)


def rank_csv_in(csv_rank_file: Path) -> list:
    with open(csv_rank_file, "r") as f:
        return [line.strip().split(",") for line in f.read().strip().split("\n")]


def main(sdf_file: Path, csv_rank_file: Path, csv_file: Path):
    """Takes in an SDF file, calculates a number of statistics, and places into a csv file

    CSV file format:


    Args:
        sdf_file: the concat SDF file with all molecules
        csv_rank_file: CSV with all molecules listed in ranked order
            Index = index in sdf_file
        csv_file: csv file location
            Will create folder if it does not exist
    """
    # read in the molecules
    molecules = Chem.SDMolSupplier(
        str(sdf_file), sanitize=True, removeHs=False, strictParsing=True
    )
    # setup molecule analysis
    models_dir: Path = (Path(__file__).parent / "models").resolve()
    logs_list: list[float] = calculate_logs(molecules, models_dir)
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
