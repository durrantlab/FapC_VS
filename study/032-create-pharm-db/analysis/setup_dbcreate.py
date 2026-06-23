from pathlib import Path
import os, tempfile
import shutil

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

HEADER: str = """#!/bin/bash
#SBATCH --job-name=create_db                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=32G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/batch.out                          # Output log path

module purge
module load pixi

"""

def main(sdf_db_path: Path, db_main_path: Path, skip_file_format: bool = False):
    """Takes in library of sdf molecules, edits files to be
    correct format and creates a script that (when run)
    will setup the database

    Args:
        sdf_db_path (Path): where the sdf library is
        db_main_path (Path): where the db will be placed
    """
    
    # get all sdf files
    sdf_file_list: list[Path] = [item for item in sdf_db_path.iterdir() if item.is_file() and item.suffix == ".sdf"]

    # edit all files to have different names for each molecule
    if not skip_file_format:
        index = 0
        for sdf_file in sdf_file_list:
            print(f"fixing {sdf_file}")
            index = fix_names(sdf_file, index)
    
    # create main db if it doesnt exist
    if not db_main_path.is_dir():
        db_main_path.mkdir(parents=True, exist_ok=True)

    # create the job list
    job_list_path: Path = (DIR_SCRIPT / "job_list.txt").resolve()
    job_num = 0
    with open(job_list_path, "w") as f:
        for sdf_file in sdf_file_list:
            # determine if its respective DB exists
            db_path: Path = (db_main_path / f"{sdf_file.name.split('.')[0]}").resolve()
            if db_path.is_dir():
                # determien if valid
                if (db_path / "dbinfo.json").resolve().exists():
                    print(f"{db_path.name} is already valid")
                    continue
                else:
                    print(f"{db_path.name} is invalid. Deleting")
                    shutil.rmtree(db_path)
            else:
                print(f"{db_path.name} does not exist yet")
            # if doesnt exist / was invalid (and deleted)
            f.write(f"-dbdir {db_path} -in {sdf_file}\n")
            job_num = job_num + 1

    # create bash to run db creator
    bash_path: Path = (DIR_SCRIPT / "create_db.sh").resolve()
    with open(bash_path, "w") as f:
        f.write(f"sbatch --array=0-{job_num-1} --export=ALL create_db.slurm")



def fix_names(sdf_file: Path, index: int) -> int:
    next_line = True
    with open(sdf_file) as src, \
        tempfile.NamedTemporaryFile("w", delete=False, dir=sdf_file.parent.resolve(), newline="") as tmp:
        tmpname = tmp.name
        
        for line in src:                       
            if next_line:
                tmp.write(f"mol_i{index:07d}\n")
                index = index+1
                next_line = False 
            #elif line.startswith("  Mrv"):
            #    tmp.write(line + "\n")
            #elif line.startswith("  Mrv"):
            #    split_line = line.split("_")
            #    if(len(split_line) > 1):
            #        tmp.write(" ".join(split_line[0:-1]) + "          ")
            #    else:
            #       tmp.write(line)""" # this is to fix a previous mistake i did : )
            else:
                tmp.write(line)

            if line.startswith("$$$$"):
                next_line = True
        
    os.replace(tmpname, sdf_file)    
    
    return index        



def fix_names_arch(sdf_file: Path):
    # read in file
    with open(sdf_file, "r") as f:
        mole_list = [item.split("\n") for item in f.read().split("\n$$$$\n")]
    # for each molecule edit the name
    for molecule in mole_list:
        if len(molecule) > 10:
            name_ind = next((i for i, ln in enumerate(molecule) if "PUBCHEM_EXT_DATASOURCE_REGID" in ln), -1) + 1
            name = molecule[name_ind].strip()
            molecule[1] = f"  {name}"
    # write out molecules
    with open(sdf_file, "w") as f:
        f.write("\n&&&&\n".join(["\n".join(item) for item in mole_list]))




if __name__ == "__main__":
    # inputs
    sdf_db_path: Path = Path("/ihome/jdurrant/irh24/Projects/molport_cmpds").resolve()
    #sdf_db_path: Path = Path("F:\\FapC_VS\\study\\032-create-pharm-db\\data\\").resolve() # for testing
    #db_main_path: Path = (DIR_SCRIPT / ".." / "data" / "DB").resolve()
    db_main_path: Path = Path("/ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB").resolve()

    main(sdf_db_path, db_main_path, True)


