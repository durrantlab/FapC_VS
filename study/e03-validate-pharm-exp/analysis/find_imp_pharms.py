from pathlib import Path
import sys

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = (DIR_SCRIPT  / ".." / "..").resolve()
FILE_LOG: Path = (DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log").resolve()

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "031-validate-pharm-top-div" / "analysis").resolve()))
import find_imp_pharms

if __name__ == "__main__":
    # inputs
    sdf_path: Path = (DIR_STUDY / "026-compare-sets" / "data" / "exp_set.sdf").resolve()
    csv_path: Path = (DIR_STUDY / "062-key-exp-inter" / "data" / "exp_set_interacts.csv").resolve()
    pharm_json_path: Path = (DIR_STUDY / "063-pharms-exp-set" / "data" / "exp_set.json").resolve()
    op_pharm_dir: Path = (DIR_SCRIPT / ".." / "data" / "script_output").resolve()
    op_csv_path: Path = (DIR_SCRIPT / ".." / "data" / "pharm_disable.csv")

    find_imp_pharms.main(sdf_path, csv_path, pharm_json_path, op_pharm_dir, op_csv_path, FILE_LOG)
5

