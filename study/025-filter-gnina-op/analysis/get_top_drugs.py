from pathlib import Path
import csv

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


def main(docked_dir: Path, csv_rank_file: Path, best_drugs_dir: Path):
    """Will take in the best drugs csv, and for each region (box) it will
    find the top 10 best. It will output them into a csv and give the SDFs
    seperately

    Args:
        docked_dir (Path): where the docked SDFs are
        csv_rank_file (Path): where the ranking csv is
        best_drugs_dir (Path): where the best drug data will be placed
    """

    # read in the csv
    with open(csv_rank_file, "r") as f:
        headers: list[str] =f.read().split("\n")[0].split(",")
    with open(csv_rank_file, "r") as f:
        ranking: list[list] = [item.split(",") for item in f.read().split("\n")[1:] if len(item) > 5]
    
    # get all regions
    regions: list[str] = [p.name for p in docked_dir.iterdir() if p.is_dir()]
    
    best_drugs: dict[str, dict] = {}
    for region in regions:
        best_drugs[region] = []
    
    # get the best molecules in each region
    for molecule in ranking:
        region: str = molecule[1]
        if len(best_drugs[region]) < 10:
            best_drugs[region].append(molecule)
    
    if not best_drugs_dir.is_dir():
        best_drugs_dir.mkdir(parents=True, exist_ok=True)

    # write the best drugs for each region
    for region, best_drugs in best_drugs.items():
        csv_op_file: Path = Path(best_drugs_dir / f"{region}_best.csv").resolve()
        with open(csv_op_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            
            writer.writerow(headers)
            writer.writerows(best_drugs)

    # TODO: extract the best SDFs as singular SDFs for each region and place them




if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(DIR_STUDY / "024-dock-div-set" / "data" / "docked_compounds")
    csv_rank_file: Path = Path(DIR_STUDY / "025-filter-gnina-op" / "data" / "ranked_docked_mols.csv")
    best_drugs: Path = Path(DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs")
    
    main(docked_dir, csv_rank_file, best_drugs)


