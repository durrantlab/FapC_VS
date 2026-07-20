
from pathlib import Path
from FapC_VS.pharmit import create_batch_iterative_pharm_job

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # base directories
    base_disabled_pharmit_dir: Path = (
        DIR_STUDY / "c03-validate-pharm-top-div" / "data" / "visual_inspect"
    ).resolve()
    base_pharmit_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "search_output").resolve()

    # go through every region and run create batch job
    create_batch_iterative_pharm_job.main(base_disabled_pharmit_dir, 
        base_pharmit_output_dir, DIR_STUDY, 2000)
