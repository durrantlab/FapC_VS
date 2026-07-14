from pathlib import Path
import logging


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


def main():
    pass






if __name__ == "__main__":
    # inputs
    
    exp_ligands_dir: Path = (DIR_STUDY / "026-compare-sets" / "data").resolve()
    protein_file: Path = (DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb").resolve()
    op_dir: Path = (DIR_STUDY / "062-key-exp-inter" / "data").resolve()

    main()


