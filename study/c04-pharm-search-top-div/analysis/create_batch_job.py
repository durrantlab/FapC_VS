
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
    disabled_pharmit_dirs: list[Path] = [
        item
        for item in base_disabled_pharmit_dir.iterdir()
        if item.is_dir() and item.name.startswith("region")
    ]
    for disabled_pharmit_dir in disabled_pharmit_dirs:
        region: str = disabled_pharmit_dir.stem
        pharmit_output_dir = (base_pharmit_output_dir / region).resolve()
    create_batch_iterative_pharm_job.main(disabled_pharmit_dir, pharmit_output_dir, 
        DIR_STUDY, 2000)
