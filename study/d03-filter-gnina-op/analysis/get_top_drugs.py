import csv
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


def main(docked_dir: Path, csv_rank_file: Path, best_drugs_dir: Path, num_best: int):
    """Will take in the best drugs csv, and it will find the overall top X best.
    It will output them into a csv and give the SDFs seperately + concatted

    Args:
        docked_dir: where the docked SDFs are
            Will search recursively
        csv_rank_file: where the ranking csv is
        best_drugs_dir: where the best drug data will be placed
            Will create directory if it does not exist
            Adds in 'singles' directory with all molecules by themselves
            Creates a overall_concat.sdf with all of them inside
        num_best: how many total molecules
    """

    # read in the csv
    with open(csv_rank_file, "r") as f:
        text: list[str] = f.read().strip().split("\n")
        headers: list[str] = text[0].split(",")
        ranking: list[list] = [item.split(",") for item in text[1:] if len(item) > 5]

    best_drugs: list[list] = []

    # get the best molecules in each region
    for molecule in ranking:
        if len(best_drugs) < num_best:
            best_drugs.append(molecule)

    if not best_drugs_dir.is_dir():
        best_drugs_dir.mkdir(parents=True, exist_ok=True)

    # write the best drugs
    csv_op_file: Path = Path(best_drugs_dir / f"overall_best.csv").resolve()
    with open(csv_op_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(best_drugs)

    # extract the best SDFs as singular SDFs for each region and place them
    sdf_path: Path = Path(best_drugs_dir / "singles").resolve()
    if not sdf_path.is_dir():
        sdf_path.mkdir(parents=True, exist_ok=True)
    for rank_num, best_drug in enumerate(best_drugs):
        sdf_data: str = extract_molecule(best_drug, docked_dir)
        specific_path: Path = Path(sdf_path / f"r{rank_num:02d}_{best_drug[4]}.sdf")
        with open(specific_path, "w") as f:
            f.write(sdf_data + "\n\n$$$$")
        concat_sdf_file: Path = Path(best_drugs_dir / f"overall_concat.sdf").resolve()
    concat_sdfs(sdf_path, concat_sdf_file)


def concat_sdfs(lig_inp_dir: Path, lig_op_file: Path):
    """Will take in a list of ligands and combine into
    n_sdf number of sdf files. Number of SDF files should
    be how many total jobs will be run

    Args:
        lig_inp_dir: Where ligands by themselves are found
        lig_op_dir: Where ligands together will be placed
        n_sdf: number of together SDF files to be made
    """
    lig_list: list[Path] = [item for item in lig_inp_dir.iterdir() if item.is_file()]
    lig_list.sort()

    towrite = ""
    for lig in lig_list:
        with open(lig, "r") as f:
            toadd: str = f.read().strip()
            towrite = towrite + toadd + "\n"

        with open(lig_op_file, "w") as f:
            f.write(towrite.strip())


def extract_molecule(drug: list, docked_dir: Path) -> str:
    """Will take in drug data and extract its specific molecule
    / pose from the docked sdfs

    Args:
        drug: holds data about drug.
            cnn_vs,directory,file_name,pose_ind,name
        docked_dirt: holds path with all docked sdfs

    Returns:
        str: the sdf data
    """

    full_path: Path = Path(docked_dir / drug[1] / f"{drug[2]}")
    with open(full_path, "r", encoding="utf-8") as f:
        all_drugs: list = [item.strip() for item in f.read().strip().split("$$$$")]
    return all_drugs[int(drug[3])]


if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "051-dock-pharm-div-set" / "data" / "docked_compounds"
    )
    csv_rank_file: Path = Path(
        DIR_STUDY / "061-filter-gnina-op" / "data" / "ranked_docked_mols.csv"
    )
    best_drugs: Path = Path(DIR_STUDY / "061-filter-gnina-op" / "data" / "best_drugs")

    main(docked_dir, csv_rank_file, best_drugs, 100)
