from pathlib import Path
from FapC_VS.pharmit import create_pharm_inp

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    top_div_set_dir: Path = (
        DIR_STUDY / "b03-filter-gnina-op" / "data" / "best_drugs"
    ).resolve()
    output_dir: Path = (DIR_STUDY / "c02-pharms-top-div-set" / "data").resolve()

    create_pharm_inp.main(top_div_set_dir, output_dir, DIR_SCRIPT)
