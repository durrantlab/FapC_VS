from pathlib import Path

from FapC_VS.gnina import rank_docked

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "b02-dock-div-set" / "data" / "docked_compounds"
    )
    csv_op_file: Path = Path(
        DIR_STUDY / "b03-filter-gnina-op" / "data" / "ranked_docked_mols.csv"
    )

    rank_docked.main(docked_dir, csv_op_file)
