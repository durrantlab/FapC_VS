from pathlib import Path
from FapC_VS.pharmit import find_imp_pharms

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = (DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


if __name__ == "__main__":
    # inputs
    sdf_path: Path = (DIR_STUDY / "b04-compare-sets" / "data" / "exp_set.sdf").resolve()
    csv_path: Path = (
        DIR_STUDY / "e01-key-exp-inter" / "data" / "exp_set_interacts.csv"
    ).resolve()
    pharm_json_path: Path = (
        DIR_STUDY / "e02-pharms-exp-set" / "data" / "exp_set.json"
    ).resolve()
    op_pharm_dir: Path = (DIR_SCRIPT / ".." / "data" / "script_output").resolve()
    op_csv_path: Path = DIR_SCRIPT / ".." / "data" / "pharm_disable.csv"

    find_imp_pharms.main(
        sdf_path, csv_path, pharm_json_path, op_pharm_dir, op_csv_path, FILE_LOG
    )
5
