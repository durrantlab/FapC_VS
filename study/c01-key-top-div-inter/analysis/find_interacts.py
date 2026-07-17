from pathlib import Path
from fapc.pharmit import find_key_interact

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    docked_ligands_dir: Path = (
        DIR_STUDY / "b03-filter-gnina-op" / "data" / "best_drugs"
    ).resolve()
    protein_file: Path = (
        DIR_STUDY / "b01-prep-protein-dock" / "data" / "9nqd_protonated.pdb"
    ).resolve()
    op_dir: Path = (DIR_SCRIPT / ".." / "data").resolve()
    find_key_interact.main(docked_ligands_dir, protein_file, op_dir)
