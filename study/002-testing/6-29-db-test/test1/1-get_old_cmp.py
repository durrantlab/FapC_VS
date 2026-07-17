import sys
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


# add the parent directory to the import search path
LIB_PATH: Path = (
    Path(__file__) / ".." / ".." / ".." / ".." / "033-pharm-search-top-div" / "analysis"
).resolve()
sys.path.insert(0, str(LIB_PATH))
import iterative_pharm


def main(
    pharm_list_file: Path,
    pharm_db_dir: Path,
    pharmit_output_dir: Path,
    temp_dir: Path,
    max_mol: int,
) -> None:
    iterative_pharm.main(
        pharm_list_file, pharm_db_dir, pharmit_output_dir, temp_dir, max_mol
    )


if __name__ == "__main__":
    pharm_list_file: Path = (DIR_SCRIPT / "reg_1_mol1_base_input.json").resolve()
    """The location of the pharmit search input (pharmacophore list) that is
    being searched. Will be input via command line"""

    pharm_db_dir: Path = Path("/ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB").resolve()
    """where the pharmit database is stored"""

    pharmit_output_dir: Path = (DIR_SCRIPT / "output").resolve()
    """where the pharmit search output will be stored"""

    temp_dir: Path = (DIR_SCRIPT / "temp").resolve()
    """where temporary files will be stored"""

    max_mol: int = 2000
    """the max number of results for a molecule"""
    main(pharm_list_file, pharm_db_dir, pharmit_output_dir, temp_dir, max_mol)
