from pathlib import Path

from FapC_VS.gnina import find_similarity

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    top_div_set_dir: Path = Path(
        DIR_STUDY / "b03-filter-gnina-op" / "data" / "best_drugs"
    )
    exp_set_file: Path = Path(DIR_SCRIPT / ".." / "data" / "exp_set.sdf")
    op_dir: Path = Path(DIR_SCRIPT / ".." / "data")

    find_similarity.main(top_div_set_dir, exp_set_file, op_dir)
