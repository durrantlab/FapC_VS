import sys
from pathlib import Path
DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


# add the parent directory to the import search path
LIB_PATH: Path = (Path(__file__) / ".." / ".." / ".." / ".." / "032-create-pharm-db" / "analysis").resolve()
sys.path.insert(0, str(LIB_PATH))
import setup_dbcreate


def main(sdf_db_path: Path, db_main_path: Path, skip_file_format: bool = False):
    setup_dbcreate.main(sdf_db_path, db_main_path, skip_file_format, DIR_SCRIPT)





if __name__ == "__main__":
    # inputs
    sdf_db_path: Path = Path(DIR_SCRIPT / "db_mols").resolve()
    #sdf_db_path: Path = Path("F:\\FapC_VS\\study\\032-create-pharm-db\\data\\").resolve() # for testing
    #db_main_path: Path = (DIR_SCRIPT / ".." / "data" / "DB").resolve()
    db_main_path: Path = Path(DIR_SCRIPT / "DB").resolve()

    main(sdf_db_path, db_main_path, True)