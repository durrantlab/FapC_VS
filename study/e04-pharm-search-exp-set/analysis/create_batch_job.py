import shutil
import sys
from pathlib import Path
from FapC_VS.pharmit import create_batch_iterative_pharm_job

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    disabled_pharmit_dir: Path = (
        DIR_STUDY / "e03-validate-pharm-exp" / "data" / "visual_inspect"
    ).resolve()
    pharmit_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "search_output").resolve()
    pharm_search_base: Path = (DIR_SCRIPT / "pharm_search_BASE.slurm").resolve()
    iterative_pharm_loc: Path = (
        DIR_STUDY / "c04-pharm-search-top-div" / "analysis" / "iterative_pharm.py"
    ).resolve()

    create_batch_iterative_pharm_job.main(
        disabled_pharmit_dir,
        pharmit_output_dir,
        DIR_SCRIPT,
        5000,
    )
