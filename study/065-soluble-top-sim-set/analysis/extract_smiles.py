from pathlib import Path
from rdkit import Chem
import csv
from rdkit.Chem import AllChem

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

def main(sdf_file: Path, csv_file: Path):
    """Takes in a concated SDF file and returns a CSV file
    where index = order in sdf, and lists:
    Name, CNN, Smiles

    Args:
        sdf_file (Path): concat SDF file
        csv_file (Path): csv file being exported into
            Name, CNN, SMILES
            Order is same as order in SDF
            Creates directory if does not exist
    """ 
    with open(sdf_file, "rb") as handle:
        # sanitize=False: we only read text fields, so don't drop records that
        # would fail chemical sanitization -- the properties are still readable.
        reader = Chem.ForwardSDMolSupplier(handle, removeHs=False, sanitize=False)

        if not csv_file.parent.exists():
            csv_file.parent.mkdir(parents=True, exist_ok=True)


        with open(csv_file, "w", newline="") as out:   # newline="" avoids blank rows on Windows
            writer = csv.writer(out)
            writer.writerow(["SMILES"])
            for i, mol in enumerate(reader):
                if mol is None:
                    # record couldn't be parsed at all -- skip it
                    continue
 
                name = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else f"mol_{i}"
                smiles = mol.GetProp("SMILES").strip() if mol.HasProp("SMILES") else ""
                cnn = mol.GetProp("CNNscore").strip() if mol.HasProp("CNNscore") else ""
 
                writer.writerow([smiles])


if __name__ == "__main__":
    sdf_file: Path = (DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs" / "overall_concat.sdf").resolve()
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "SMILES.csv").resolve()
    
    main(sdf_file, csv_file)