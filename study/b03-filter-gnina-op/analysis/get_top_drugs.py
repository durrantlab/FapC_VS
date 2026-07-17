
from pathlib import Path
from FapC_VS.gnina import get_top_drugs

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "b02-dock-div-set" / "data" / "docked_compounds"
    )
    csv_rank_file: Path = Path(
        DIR_SCRIPT / ".." / "data" / "ranked_docked_mols.csv"
    )
    best_drugs: Path = Path(DIR_SCRIPT / ".." / "data" / "best_drugs")

    get_top_drugs.main(docked_dir, csv_rank_file, best_drugs, 10)
