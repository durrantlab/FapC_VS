from pathlib import Path
import sys

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()
FILE_LOG: Path = (DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log").resolve()

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "065-stats-top-sim-set" / "analysis").resolve()))
import get_top_drugs


if __name__ == "__main__":
    # inputs
    sdf_file: Path = (DIR_STUDY / "069-filter-gnina-op-pharm-exp" / "data" / "best_drugs" / "overall_concat.sdf").resolve()
    csv_rank_file: Path = (DIR_STUDY / "069-filter-gnina-op-pharm-exp" / "data" / "best_drugs" / "overall_best.csv").resolve()
    models_dir: Path = (DIR_SCRIPT / "models")
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "top_dock_stats.csv").resolve()
    get_top_drugs.main(sdf_file, csv_rank_file, models_dir, csv_file)


