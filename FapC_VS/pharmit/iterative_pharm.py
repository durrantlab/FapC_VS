import json
import shutil
from copy import copy, deepcopy
from pathlib import Path

import pharmit_server_query


def main(
    pharm_list_file: Path, sdf_file: Path, csv_file: Path, temp_dir: Path, max_mol: int
):
    """Using 1 pharmacophore list input will iteratively run pharmacophore searches
    with pharmit, removing pharmacophores in BFS style, until only 3 remain or
    max_mol compounds are found.

    Will place all data in a single sorted sdf and sorted csv, specified in input

    Args:
        pharm_list_file: The location of the pharmit search input
            (pharmacophore list) that is being searched.
        sdf_file: where SDF file output of pharmit will be stored (sorted, only 1 made)
            Has format of typical concatenated SDF file
            Will create directory path if not present
        csv_file: Where CSV file output of pharmit will be stored (sorted, only 1 made)
            Header is [# of mols],name,rmsd. Each row is a different molecule,
            storing it's index, name and RMSD
            Will create directory path if not present
        temp_dir: where temporary files will be stored
            This is deleted before and after. Make sure it does not overlap with
            other parallel runs. Holds temp sdf, csv outputs and inputs to pharmit
            Will create directory path. Should not be present before hand.
        max_mol: max molecules to find
    """
    # setup iterative pharm data structure. Allows going through different
    # combinations of pharmacophore lists
    print(f"ITERATIVE PHARM ON: {pharm_list_file}")
    pharm_obj: iter_pharm = iter_pharm(pharm_list_file, temp_dir)

    # create temp_dir / pharmit_output dir
    if temp_dir.is_dir():
        print("WARNING: TEMP DIR IS ALREADY PRESENT. DELETING.")
        shutil.rmtree(temp_dir)  # only works on linux
        pass
    temp_dir.mkdir(parents=True, exist_ok=True)
    if not sdf_file.parent.is_dir():
        sdf_file.parent.mkdir(parents=True, exist_ok=True)
    if not csv_file.parent.is_dir():
        csv_file.parent.mkdir(parents=True, exist_ok=True)

    # setup up data csv. Stores info about all molecules present
    csv_file: Path = csv_setup(csv_file)
    sdf_files: list[Path] = []

    # while count of molecules stored less then < 2000, check more pharm combs
    total_mol = 0
    first_run = True
    while total_mol < max_mol:
        # create input for pharmit. If invalid, break.
        if first_run:
            iter_name = "none"
            first_run = False
        else:
            iter_name: str = pharm_obj.next_pharm()
            if iter_name == "invalid":
                print("no more valid combinations left")
                break
        pharm_file: Path = pharm_obj.write_curr_json()
        print(f"\nSearching with pharm config: disabled {iter_name}")
        # run pharmit with pharm file
        success, op_sdf_file, op_csv_file = run_pharmit(
            pharm_file,
            temp_dir,
            f"op_{iter_name}",
            max_mol - total_mol + (max_mol // 4),
        )
        # update list of SDF / csv if pharmit found molecules
        if success:
            sdf_files.append(op_sdf_file)
            total_mol: int = update_csv(op_csv_file, csv_file, max_mol)

    # sort csv and concat sdfs
    print("\nSorting csv file")
    sort_csv(csv_file)
    concat_sdfs(sdf_files, sdf_file, csv_file)
    shutil.rmtree(temp_dir)
    print("Done!")


def concat_sdfs(sdf_files: list[Path], sdf_file: Path, csv_file: Path):
    """Takes in all SDF files output (in temp dir) and
    brings them together into a single sorted sdf_file. No
    duplicates

    Args:
        sdf_files (list[Path]): where all SDFs output from
            pharmit are stored
        sdf_file: the final SDF file where all molecules
            are stored in sorted format. No duplicates.
    """
    with open(csv_file) as f:
        csv: list[list[str]] = [
            [item2 for item2 in item.strip().split(",")]
            for item in f.read().strip().split("\n")
        ]
    # read in all current sdfs
    mols: list[list[str]] = []
    for pharm_sdf in sdf_files:
        with open(pharm_sdf, "r") as f2:
            mols.extend(
                [mol.strip().split("\n") for mol in f2.read().strip().split("$$$$")]
            )
    # write out the concat, sorted SDF file
    with open(sdf_file, "w") as f:
        f.write("")
    with open(sdf_file, "a") as f1:
        # go through each line in csv, then find that molecule in all SDF files
        for line in csv:
            for mol in mols:
                if mol[0] == line[1]:
                    f1.write("\n".join(mol) + "\n\n$$$$\n")
                    break


def sort_csv(csv_path: Path):
    """Takes in a csv file and sorts it based rmsd (col2)

    Args:
        csv_path: where the csv file is currently placed
    """
    # read in csv file
    with open(csv_path) as f:
        csv: list[list[str]] = [
            [item2 for item2 in item.strip().split(",")]
            for item in f.read().strip().split("\n")
        ]
    csv_head: list[str] = csv[0]
    # sort body of csv
    csv_body: list[list[str]] = csv[1:]
    csv_body.sort(key=lambda x: float(x[2]))
    # add in indicies
    for mol_ind in range(len(csv_body)):
        csv_body[mol_ind][0] = str(mol_ind)
    # write out csv
    csv = [csv_head] + csv_body
    with open(csv_path, "w") as f:
        text: str = "\n".join([",".join(item) for item in csv])
        f.write(text)


def update_csv(pharm_csv_op: Path, csv_file: Path, max_num: int) -> int:
    """Updates CSV based on the pharmit search

    Args:
        pharm_op: where the pharmit search op is
        csv_file: where the csv file is
        max_num: max number of molecules to return
    """
    # open up files
    file_name: str = pharm_csv_op.stem
    with open(pharm_csv_op, "r") as f:
        csv_pharm: list[list[str]] = [
            [item2 for item2 in item.strip().split(",")]
            for item in f.read().strip().split("\n")
        ][1:]
    with open(csv_file, "r") as f:
        csv_final: list[list[str]] = [
            [item2 for item2 in item.strip().split(",")]
            for item in f.read().strip().split("\n")
        ]
    # calculate number of total molecules
    mol_num = int(csv_final[0][0])
    # add each molecule, if not already inside
    for mol in csv_pharm:
        name: str = mol[0]
        rmsd: str = mol[1]
        if not already_inside_csv(csv_final, name):
            csv_final.append(["0", name, str(rmsd), file_name])
            mol_num = mol_num + 1
        if mol_num == max_num:
            break
    csv_final[0][0] = str(mol_num)
    # write out csv
    with open(csv_file, "w") as f:
        text: str = "\n".join([",".join(item) for item in csv_final])
        f.write(text)
    return mol_num


def already_inside_csv(csv: list[list[str]], name: str):
    for line in csv[1:]:
        if line[1] == name:
            return True
    return False


def run_pharmit(
    pharm_file: Path, pharmit_output_dir: Path, run_name: str, max_mol: int
) -> tuple[bool, Path, Path]:
    """Takes in pharmit inputs, and sends it to the server. Creates
    an SDF with all hits of out order, and csv with each molecule's
    RMSD and name.

    CSV's 1st row is 'name,rmsd', past that is each different molecules
    name / rmsd. Ends with a \n

    Args:
        pharm_file: where pharm input is located
        pharmit_output_dir: where all output for this molecule is placed
                                Name based on pharm file path / name
                                Creates a CSV and SDF in this directory
        run_name: name of the specific pharmacohpore iteration. Refers to
                        which pharmacophores are disabled
        max_mol: max # of molecules that can be returned

    Returns:
        Bool: if pharmit found molecules succesfully
        Path1: SDF file where molecules were placed
        Path2: CSV file where molecules are listed
    """
    # create output files
    final_sdf: Path = (pharmit_output_dir / f"{run_name}.sdf").resolve()
    """Where SDF outputs of search are held. Random order, not based on RMSD."""
    final_csv: Path = (pharmit_output_dir / f"{run_name}.csv").resolve()
    """Where SDF outputs of search are held. Form of name, RMSD"""

    # run pharmit
    success = pharmit_server_query.run(
        pharm_file, final_sdf, 16, 500, final_csv, max_mol
    )

    return success, final_sdf, final_csv


def already_inside_csv(csv: list[list], name: str) -> bool:
    if name in [line[1] for line in csv]:
        return True
    return False


def fake_pharmit(cmd: list[str]):
    """Just meant to replicate what pharmit would do if I could run it"""
    to_copy: Path = Path(
        "D:\\FapC_VS\\study\\c04-pharm-search-top-div\\data\\search_output\\op_all.sdf"
    ).resolve()
    shutil.copy2(to_copy, Path(cmd[12]))


def csv_setup(csv_file: Path) -> Path:
    """Create a csv that stores data about run.
    Header: total_count
    Body: rank, molecule name, rmsd

    Args:
        csv_file: the csv file path
    """

    with open(csv_file, "w") as f:
        f.write("0,name,rmsd,search_iteration")
    return csv_file


class iter_pharm:
    """Will take in a list of pharmacophores, and allow for
    iteration through different combinations of disabled
    pharmacophores in a BFS manor (i.e. all possible single
    disabled, all possible 2 groups disabled).

    Can then write it to file to be used by pharmit"""

    base_json: dict
    """What the original json looks like"""
    disable_list: list[int]
    """Each index is a different pharmacophore  that
    is disabled. The number stored is the index of the pharm
    that is disabled"""
    pharm_ind_dict: list[int]
    """takes in index from disable list and translates to 
    real index in the base json"""
    temp_dir: Path
    """the temp pharm jsons file"""
    num_base_pharms: int
    """how many pharms are enabled in base json"""

    def __init__(self, pharm_list_file: Path, temp_dir: Path):
        """Takes in the base pharm list and creates iter_pharm.
        Initilizes the disable list so nothing is disabled
        Setups dictionary to allow translation

        Args:
            pharm_list_dir: The location of the pharmit search input
                                   (pharmacophore list) that is being searched.
            temp_dir: where the pharmit search output will be stored
        """
        with open(pharm_list_file, "r", encoding="utf-8") as f:
            self.base_json = json.loads(f.read())
        self.disable_list = []
        self.temp_dir = temp_dir
        self.pharm_ind_dict = []
        for p_index, pharm in enumerate(self.base_json["points"]):
            if pharm["enabled"]:
                self.pharm_ind_dict.append(p_index)
        self.num_base_pharms = len(self.pharm_ind_dict)

    def get_curr_json(self) -> dict:
        """Based on current state of disable list
        returns the json with right pharms disabled

        Returns:
            dict: json with right pharms disabled
        """
        temp_dict = deepcopy(self.base_json)
        for index in self.disable_list:
            pharm_index = self.pharm_ind_dict[index]
            temp_dict["points"][pharm_index]["enabled"] = False
        return temp_dict

    def next_pharm(self):
        """Will go to next disable state in the
        'BFS'
        """
        # if first next, setup so it disables 0 first
        if len(self.disable_list) == 0:
            self.disable_list.append(-1)
        # loop until no repeats in number list
        while True:
            self.disable_list[0] = self.disable_list[0] + 1
            for ind in range(len(self.disable_list)):
                if self.disable_list[ind] >= self.num_base_pharms:
                    self.disable_list[ind] = 0
                    if ind + 1 >= len(self.disable_list):
                        self.disable_list.append(0)
                    self.disable_list[ind + 1] = self.disable_list[ind + 1] + 1
            if len(self.disable_list) > self.num_base_pharms - 3:
                return "invalid"
            if len(self.disable_list) == len(set(self.disable_list)):
                break
        return self.dis_list_to_str()

    def write_curr_json(self) -> Path:
        """Takes in the current json and
        writes it to temp folder
        """
        curr_json: dict = self.get_curr_json()
        json_str: str = json.dumps(curr_json)
        dis_name: str = self.dis_list_to_str()
        if dis_name == "":
            dis_name = "none"
        temp_file = Path(self.temp_dir / f"dis_{dis_name}.json").resolve()
        with open(temp_file, "w") as f:
            f.write(json_str)
        return temp_file

    def dis_list_to_str(self) -> str:
        """Takes in disable list and returns str

        Returns:
            str: str var of disable list
        """
        return "-".join([str(item) for item in self.disable_list])