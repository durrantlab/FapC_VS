from pathlib import Path
import logging
from rdkit import Chem
import csv

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



def main(sdf_file: Path, csv_file: Path):
    # read in the molecules
    molecules = Chem.SDMolSupplier(str(sdf_file), sanitize=True, removeHs=False,
                            strictParsing=True)
    # get information about molecules
    data: list = []
    data.append(predefined_models.predefined_mordred(None, "best", True))
    for molecule in molecules:
        data.append(predefined_models.predefined_mordred(molecule, "best", False)) 

    with open(csv_file, "w", newline="") as f:
        csv.writer(f).writerows(data)


if __name__ == "__main__":
    # inputs
    sdf_file: Path = (DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs" / "overall_concat.sdf").resolve()
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "solubility.csv").resolve()
    main(sdf_file,csv_file )


