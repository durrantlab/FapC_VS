from pathlib import Path

from FapC_VS.gnina import molecule_statistics

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    sdf_file: Path = (
        DIR_STUDY / "d03-filter-gnina-op" / "data" / "best_drugs" / "overall_concat.sdf"
    ).resolve()
    csv_rank_file: Path = (
        DIR_STUDY / "d03-filter-gnina-op" / "data" / "best_drugs" / "overall_best.csv"
    ).resolve()
    csv_file: Path = (DIR_SCRIPT / ".." / "data" / "top_dock_stats.csv").resolve()
    molecule_statistics.main(sdf_file, csv_rank_file, csv_file)
