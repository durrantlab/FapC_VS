import csv
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


def main(docked_dir: Path, csv_op_file: Path):
    """Will take in all docked molecules (recursively) in a directory, determine 
    the best pose for each and store the score. Will then order on score. 
    Places order in a csv

    Args:
        docked_dir: Where all the docked molecules are stored
            Can be in subdirectory
        csv_op_file: Where the ranks will be output
            Will create file if doesnt exist
    """

    # create list of all files in all box folders
    docked_file_list: list[Path] = [
        item
        for item in docked_dir.rglob("*")
        if item.is_file() and item.suffix == ".sdf"
    ]

    # go through each instance, extract data and store in dictionary for that
    pose_dict = get_pose_data(docked_dir, docked_file_list)

    # for each molecule, add the best to new list
    best_for_each: list[dict] = []
    for name, all_mols in pose_dict.items():
        # for each instance of this molecule
        to_add: dict = max(all_mols, key=lambda x: x["cnn_vs"])
        to_add["name"] = name
        best_for_each.append(to_add)

    # sort based on best scores and output as csv
    sorted_best: list[dict] = sorted(
        best_for_each, key=lambda x: x["cnn_vs"], reverse=True
    )

    # print sorted best
    headers = sorted_best[0].keys()
    if not csv_op_file.parent.is_dir():
        csv_op_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_op_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(sorted_best)


def get_pose_data(
    docked_dir: Path, docked_file_list: list[Path]
) -> dict[str, list[dict]]:
    """Will take in list of all SDFs, and organize them into a dict

    Args:
        docked_file_list: list of all SDF paths

    dict: each molecule is D1. Then it stores each instance of that molecule.
    For each instance it stores CNN_VS, directory of file, file name, location
    in file
    """

    pose_dict: dict[str, list[dict]] = {}
    for docked_file in docked_file_list:
        with open(docked_file, "r", encoding="utf-8") as f:
            op_str: str = f.read()
            pose_list: list[str] = [
                item.strip() for item in op_str.strip().split("$$$$")
            ][:-1]
            for index, pose_str in enumerate(pose_list):
                molecule_name, cnn_vs = extract_pose_data(pose_str)
                temp_dict: dict = {
                    "cnn_vs": cnn_vs,
                    "directory": docked_file.relative_to(docked_dir).parent,
                    "file_name": docked_file.name,
                    "pose_ind": index,
                }
                if not molecule_name in pose_dict.keys():
                    pose_dict[molecule_name] = []
                pose_dict[molecule_name].append(temp_dict)
    return pose_dict


def extract_pose_data(pose: str) -> tuple[str, float]:
    """Will take in a pose str and determine data stored in

    Args:
        pose: data of the molecule in SDF form

    str: name of molecule
    float: CNN_VS score
    """
    lines: list[str] = pose.split("\n")
    name: str = lines[0].strip()

    substring: str = "<CNN_VS>"
    index_cnn: int = next((i for i, s in enumerate(lines) if substring in s), 
                          -1) + 1
    cnn_vs: float = float(lines[index_cnn].strip())

    return name, cnn_vs


if __name__ == "__main__":
    # inputs
    docked_dir: Path = Path(
        DIR_STUDY / "024-dock-div-set" / "data" / "docked_compounds"
    )
    csv_op_file: Path = Path(
        DIR_STUDY / "025-filter-gnina-op" / "data" / "ranked_docked_mols.csv"
    )

    main(docked_dir, csv_op_file)
