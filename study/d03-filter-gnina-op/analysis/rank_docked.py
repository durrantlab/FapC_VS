import csv
import sys
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "b03-filter-gnina-op" / "analysis").resolve()))
import rank_docked

if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "d02-dock-pharm-div-set" / "data" / "docked_compounds"
    )
    csv_op_file: Path = Path(
        DIR_STUDY / "061-filter-gnina-op" / "data" / "ranked_docked_mols.csv"
    )
    rank_docked.main(docked_dir, csv_op_file)
