from pathlib import Path
DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()

# add the directory of script to path
from FapC_VS.pharmit import find_key_interact

if __name__ == "__main__":
    # inputs
    exp_ligands_dir: Path = (DIR_STUDY / "b04-compare-sets" / "data").resolve()
    protein_file: Path = (
        DIR_STUDY / "b01-prep-protein-dock" / "data" / "9nqd_protonated.pdb"
    ).resolve()
    op_dir: Path = (DIR_SCRIPT / ".." / "data").resolve()
    find_key_interact.main(exp_ligands_dir, protein_file, op_dir)
