from copy import copy, deepcopy
from pathlib import Path
import logging
import json
import subprocess
import shutil
import argparse

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()
FILE_LOG: Path = (DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log").resolve()

if not FILE_LOG.parent.is_dir():
    FILE_LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=FILE_LOG,
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)



def main(pharm_list_file: Path, pharm_db_dir: Path, pharmit_output_dir: Path, 
         temp_dir: Path, max_mol: int):
    """Using pharmacophore list input will iteratively run pharmacophore searches
    with pharmit, removing pharmacophores in BFS style, until only 3 remain or 
    2000 compounds are found

    Args:
        pharm_list_dir (Path): The location of the pharmit search input 
                               (pharmacophore list) that is being searched.
        pharm_db_dir (Path): where the pharmit database is stored
        pharmit_output_dir (Path): where temporary files will be stored
        temp_dir (Path): where the pharmit search output will be stored
    """
    # setup iterative pharm data structure
    print(f"ITERATIVE PHARM ON: {pharm_list_file}")
    pharm_obj: iter_pharm = iter_pharm(pharm_list_file, temp_dir)

    # create temp_dir / pharmit_output dir
    if temp_dir.is_dir():
        shutil.rmtree(temp_dir) # only works on linux
        pass
    temp_dir.mkdir(parents=True, exist_ok=True)
    if pharmit_output_dir.is_dir():
        shutil.rmtree(pharmit_output_dir)
        pass
    pharmit_output_dir.mkdir(parents=True, exist_ok=True)

    # setup up data csv. Stores info about all molecules present
    csv_file: Path = csv_setup(pharmit_output_dir)
    
    # while count of molecules stored less then < 2000, check more pharm combs
    total_mol = 0
    first_run = True
    while total_mol < max_mol:
        # create input for pharmit. If invalid, break.
        if first_run:
            iter_name = 'all'
            first_run = False
        else:
            iter_name: str = pharm_obj.next_pharm()
            if iter_name == 'invalid':
                print("no more valid combinations left")
                break
        pharm_file: Path = pharm_obj.write_curr_json()
        print(f"Searching with pharm config: {iter_name}")
        # run pharmit.
        op_file: Path = run_pharmit(pharm_file, pharm_db_dir, pharmit_output_dir,
                        f"op_{iter_name}", max_mol-total_mol)
        
        # determine total count and update csv
        total_mol: int = update_csv(op_file, csv_file, max_mol)

    # give info about run. End
    print("Done!")


def update_csv(pharm_op: Path, csv_file: Path, max_mol: int) -> int:
    """Updates CSV based on the pharmit search

    Args:
        pharm_op (Path): where the pharmit search op is
        csv_file (Path): where the csv file is
    """
    file_name: str = pharm_op.stem
    with open(csv_file, "r") as f:
        csv: list[list[str]] = [[item2 for item2 in item.split(",")] for item in f.read().split("\n")]
    with open(pharm_op, "r") as f:
        mol_list: list[list[str]] = [[item2 for item2 in item.strip().split("\n")] for item in f.read().split("$$$$")[:-1]]
    csv_body: list[list[str]] = []
    mol_num = int(csv[0][0]) + len(mol_list)
    for mol_ind, mol in enumerate(mol_list):
        name: str = mol[0].strip()
        rmsd: str = mol[-1].strip()
        csv_body.append(["0", name, str(rmsd), file_name, str(mol_ind)])
    csv.extend(csv_body)
    if(mol_num >= max_mol):
        csv_head: list[str] = csv[0]
        csv_body: list[list[str]] = csv[1:]
        csv_body.sort(key= lambda x: float(x[2]))
        for mol_ind in range(len(csv_body)):
            csv_body[mol_ind][0] = str(mol_ind)
        csv = [csv_head] + csv_body
    csv[0][0] = str(mol_num)
    with open(csv_file, "w") as f:
        text: str = "\n".join([",".join(item) for item in csv])
        f.write(text)
    return int(csv[0][0])



def run_pharmit(pharm_file: Path, pharm_db_dir: Path, pharmit_output_dir: Path,
                run_name: str, max_mol: int) -> Path:
    """Takes in pharmit inputs, crafts the bash command and runs it

    Args:
        pharm_file (Path): where pharm input is located
        pharm_db_dir (Path): where db is located
        pharmit_output_dir (Path): where all output for this molecule is placed
        run_name (str): name of the specific pharmacohpore iteration
        max_mol (int): max # of molecules that can be returned
    """
    # folders
    final_sdf: Path = (pharmit_output_dir / f"{run_name}.sdf").resolve()
    temp_sdf_folder: Path = (pharmit_output_dir / f"{run_name}").resolve()
    if temp_sdf_folder.is_dir():
        shutil.rmtree(temp_dir) # only works on linux
        pass
    temp_sdf_folder.mkdir(parents=True, exist_ok=True)

    # go through each database
    all_db_paths: list[Path] = [item for item in pharm_db_dir.iterdir() if item.is_dir()]
    all_temp_sdfs: list[Path] = []
    all_temp_txts: list[Path] = []
    for db_ind, db_path in enumerate(all_db_paths):
        # files
        db_name: str = "-".join(db_path.stem.split("-")[0:3])
        temp_sdf: Path = (temp_sdf_folder / f"{db_name}.sdf")
        temp_op_txt: Path = (temp_sdf_folder / f"{db_name}.txt")
        all_temp_sdfs.append(temp_sdf)
        all_temp_txts.append(temp_op_txt)
        print(f" Searching on {db_name}. ({db_ind+1}/{len(all_db_paths)})")
        # create command
        cmd: list[str] = ["pixi","run","-e","pharmit","pharmit","dbsearch","-max-weight","750",
                        "-extra-info","-sort-rmsd","-in",str(pharm_file),"-out",
                        str(temp_sdf),"-max-hits",str(max_mol),"-dbdir",str(db_path)]
        # run command
        result = subprocess.run(cmd, capture_output=True, text=True)
        # write out the console output
        with open(temp_op_txt, "w") as f:
            f.write(result.stdout)
        if result.returncode != 0:
            raise Exception(f"pharmit search failed to run. Code: {result.returncode} Err: {result.stderr}\n\n{' '.join(cmd)}")
    # compile all results together
    all_mols: list[list] = []
    for op_ind, temp_txt in enumerate(all_temp_txts):
        with open(temp_txt, "r") as f:
            text: list[list[str]] = [item.split(",") for item in f.read().split("\n") if len(item.split(",")) > 5]
            text2: list = [[int(item[0]), float(item[1]), item[4], all_temp_sdfs[op_ind]] for item in text]
            all_mols.extend(text2)
    # sort based on RMSD
    all_mols.sort(key=lambda x: x[1])
    # create sdf with all
    all_mol_sdfs: list[str] = []
    for mol_data in all_mols[0:2000]:
        with open(mol_data[3], "r") as f:
            #print(mol_data[3], mol_data[2])
            mol_sdf: str = [item.strip() for item in f.read().strip().split("$$$$") if item.strip().startswith(mol_data[2])][0]
            all_mol_sdfs.append(mol_sdf)
    with open(final_sdf, "w") as f:
        f.write("\n$$$$\n".join(all_mol_sdfs) + "\n$$$$")
    shutil.rmtree(temp_sdf_folder)
    return final_sdf



def fake_pharmit(cmd: list[str]):
    """Just meant to replicate what pharmit would do if I could run it"""
    to_copy: Path = Path("D:\\FapC_VS\\study\\033-pharm-search-top-div\\data\\search_output\\op_all.sdf").resolve()
    shutil.copy2(to_copy, Path(cmd[12]))


def csv_setup(temp_dir: Path) -> Path:
    """Create a csv that stores data about run.
    Header: total_count
    Body: rank, molecule name, rmsd

    Args:
        temp_dir (Path): where the csv file will be placed
    """
    csv_file: Path = (temp_dir / "data.csv").resolve()

    with open(csv_file, "w") as f:
        f.write("0,name,rmsd")
    return csv_file



class iter_pharm():
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
            pharm_list_dir (Path): The location of the pharmit search input 
                                   (pharmacophore list) that is being searched.
            temp_dir (Path): where the pharmit search output will be stored
        """
        with open(pharm_list_file, "r", encoding='utf-8') as f:
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
        if(len(self.disable_list) == 0):
            self.disable_list.append(-1)
        # loop until no repeats in number list
        while True:
            self.disable_list[0] = self.disable_list[0] + 1
            for ind in range(len(self.disable_list)):
                if self.disable_list[ind] >= self.num_base_pharms:
                    self.disable_list[ind] = 0
                    if ind+1 >= len(self.disable_list):
                        self.disable_list.append(0)
                    self.disable_list[ind+1] = self.disable_list[ind+1] + 1
            if(len(self.disable_list) > self.num_base_pharms - 3):
                return 'invalid'
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
        if dis_name == '':
            dis_name = 'all'
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
        






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="runs pharmit iteratively on a pharmacophore list")
    
    pharm_list_file: str = str((DIR_STUDY / "031-validate-pharm-top-div" / 
                            "data" / "visual_inspect" / "region_1" / "mol1_input.json").resolve())
    """The location of the pharmit search input (pharmacophore list) that is
    being searched. Will be input via command line"""
    parser.add_argument("pharm_list_file", default=pharm_list_file, 
                        nargs="?", help="where pharmacophore json is located")
    
    #pharm_db_dir: Path = Path(DIR_STUDY / "032-create-pharm-db" / "data" / "DB").resolve()
    pharm_db_dir: str = str(Path("/ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB-old").resolve())
    """where the pharmit database is stored"""
    parser.add_argument("pharm_db_dir", default=pharm_db_dir, 
                        nargs="?", help="where pharmit database is located")
    
    pharmit_output_dir: str = str((DIR_SCRIPT / ".." / "data" / "search_output" 
                                  / "region_1" / "mol1").resolve())
    """where the pharmit search output will be stored"""
    parser.add_argument("pharmit_output_dir", default=pharmit_output_dir, 
                        nargs="?", help="where the pharmit search output will be stored")

    temp_dir: str = str((DIR_SCRIPT / "temp" / "region_1" / "mol1").resolve())
    """where temporary files will be stored"""
    parser.add_argument("temp_dir", default=temp_dir, 
                        nargs="?", help="where temporary files will be stored")

    max_mol: int = 2000
    """the max number of results for a molecule"""
    parser.add_argument("max_mol", default=max_mol, type=int,
                        nargs="?", help="the max number of results for a molecule")
 
    args = parser.parse_args()
    main(Path(args.pharm_list_file), Path(args.pharm_db_dir), Path(args.pharmit_output_dir), 
        Path(args.temp_dir), args.max_mol)


