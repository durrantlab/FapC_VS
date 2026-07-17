from pathlib import Path
from FapC_VS.pharmit import find_imp_pharms

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = (DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


if __name__ == "__main__":
    # base files
    interaction_csv_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data").resolve()
    docked_sdfs: Path = (
        DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs"
    ).resolve()
    pharm_json_dir: Path = (DIR_STUDY / "028-pharms-top-div-set" / "data").resolve()
    op_dir: Path = (DIR_SCRIPT / ".." / "data").resolve()

    # extract regions
    regions: list[str] = []
    pharm_list: list[Path] = [
        item
        for item in pharm_json_dir.iterdir()
        if item.is_file() and item.suffix == ".json"
    ]
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)

    # for each region
    for region in regions:
        sdf_path: Path = (docked_sdfs / f"{region}_concat.sdf").resolve()
        csv_path: Path = (interaction_csv_dir / f"{region}_interacts.csv").resolve()
        pharm_json_path: Path = (pharm_json_dir / f"{region}_concat.json").resolve()
        op_pharm_dir: Path = (op_dir / "script_output" / region).resolve()
        op_csv_path: Path = (op_dir / "pharm_enabled" / f"{region}.csv").resolve()

        find_imp_pharms.main(sdf_path, csv_path, pharm_json_path, op_pharm_dir, op_csv_path, FILE_LOG)
