from pathlib import Path
import logging
import sys

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

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "041-setup-pharm-top-div-set" / "analysis").resolve()))
import setup_gypsum_run

def main(sdf_input_dir: Path, split_sdf_dir: Path, split_size: int, gypsum_sdf_dir: Path):
    """Takes in all the SDF to be gypsumed, splits into X chunks, then creates
    gypsum inputs to be run

    Args:
        sdf_input_dir: where SDF inputs are held (organized mol#.sdf)
        split_sdf_dir: where SDFs split into specific size are held
            Directory created if not already present.
            Will add mol_#/ directories to it
            If directories already exist, will skip splitting
        split_size: how many molecules are in each split
        gypsum_sdf_dir: where final gypsum outputs are held
            Directory created if not already present
            Will add region_#/mol_#/group_# directories to it
    """
    # for each region
    args_list: list[str] = []
    # for each diversity set molecule
    input_mol_files = [item for item in sdf_input_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
    for input_mol_file in input_mol_files:
        # split into chunks
        mol_split_sdf_dir: Path = (split_sdf_dir / input_mol_file.stem).resolve()
        if not mol_split_sdf_dir.is_dir():
            mol_split_sdf_dir.mkdir(parents=True, exist_ok=True)
            sdf_list: list[Path] = setup_gypsum_run.sdf_set_size_split( 
                input_mol_file, mol_split_sdf_dir, split_size)
        else:
            sdf_list: list[Path] = [item for item in mol_split_sdf_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
        # setup gypsum input for each file
        for sdf_file in sdf_list:
            mol_gypsum_sdf_dir: Path = (gypsum_sdf_dir / input_mol_file.stem / sdf_file.stem).resolve()
            if not mol_gypsum_sdf_dir.is_dir():
                mol_gypsum_sdf_dir.mkdir(parents=True, exist_ok=True)
            # if gypsum output doesnt exist, add to args list
            if not (mol_gypsum_sdf_dir / "gypsum_dl_success.sdf").is_file():
                args: str = f"-s {sdf_file} -o {mol_gypsum_sdf_dir}"
                args_list.append(args)
    
    # write the job_list
    job_list_file: Path = (DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_list_file, "w") as f:
        for ind, arg in enumerate(args_list):
            if ind:
                f.write("\n")
            f.write(arg)
    
    # create batch script to run slurm
    batch_script_file: Path = (DIR_SCRIPT / "run_gypsum.sh").resolve()
    with open(batch_script_file, "w") as f:
        f.write(f"sbatch --array=0-{len(args_list)-1} --export=ALL run_gypsum.slurm\n")



if __name__ == "__main__":
    # inputs
    sdf_input_dir: Path = (DIR_STUDY / "066-pharm-search-exp-set" / "data" / "search_output")
    """Where input SDFs are. Will search through dir for all .sdfs"""
    split_sdf_dir: Path = (DIR_SCRIPT / ".." / "data" / "split_sdf")
    """Where split SDFs to prepare for gypsum are held"""
    gypsum_sdf_dir: Path = (DIR_SCRIPT / ".." / "data" / "output_sdf")
    """Where the outputs of gypsum are held"""
    
    main(sdf_input_dir, split_sdf_dir, 250, gypsum_sdf_dir)


