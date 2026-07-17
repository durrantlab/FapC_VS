import csv
import sys
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "061-filter-gnina-op" / "analysis").resolve()))
import get_top_drugs

if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "f02-dock-pharm-exp-set" / "data" / "docked_compounds"
    )
    csv_rank_file: Path = Path(DIR_SCRIPT / ".." / "data" / "ranked_docked_mols.csv")
    best_drugs: Path = Path(DIR_SCRIPT / ".." / "data" / "best_drugs")

    get_top_drugs.main(docked_dir, csv_rank_file, best_drugs, 100)
