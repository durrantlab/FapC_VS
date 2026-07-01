import shutil
from pathlib import Path
import sys


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

sys.path.insert(0, str((DIR_STUDY / "031-validate-pharm-top-div").resolve()))


def main(main_disabled_pharmit_dir: Path, main_pharmit_output_dir: Path, max_ret_mol: int = 2000, DIR_SCRIPT: Path = DIR_SCRIPT):
    """Will take in pharmits input files and create a slurm to run the iterative pharm script

    Args:
        disabled_pharmit_dir (Path): where the inputs with disabled pharms based
            on prolif are stored
        pharmit_output_dir (Path): where final pharmit search inputs will be stored
            All inputs for 1 region will be in a file together
        max_ret_mol (int): max number of molecules to be returned per molecule
    """
    
    # read in disabled pharmits
    pharmit_inp_region_dirs: list[Path] = [item for item in main_disabled_pharmit_dir.iterdir() if item.is_dir() and item.name.startswith("region")]
    regions: list[str] = []
    pharmit_input_files = []
    for pharmit_inp_dir in pharmit_inp_region_dirs:
        region: str = pharmit_inp_dir.name
        regions.append(region)
        pharmit_input_files.extend([item for item in pharmit_inp_dir.iterdir() if item.is_file() and item.suffix == ".json"])

    # create the python inputs
    pharmit_inputs: list[str] = []
    for pharmit_json in pharmit_input_files:
        # setup inputs
        region: str = pharmit_json.parent.name
        mol_name: str = pharmit_json.stem.split("_")[0]
        
        pharm_list_file: Path = pharmit_json
        sdf_file: Path = (main_pharmit_output_dir / region / f"{mol_name}.sdf").resolve()
        csv_file: Path = (main_pharmit_output_dir / region / f"{mol_name}.csv").resolve()
        temp_dir: Path = (DIR_SCRIPT / "temp" / region / mol_name)
        max_mol: int = max_ret_mol

        # create OP directories
        if temp_dir.is_dir():
            shutil.rmtree(temp_dir) # only works on linux
        temp_dir.mkdir(parents=True, exist_ok=True)
        if sdf_file.parent.is_dir():
            shutil.rmtree(sdf_file.parent)
        sdf_file.parent.mkdir(parents=True, exist_ok=True)

        # string
        input_str: str = f"{pharm_list_file} {sdf_file} {csv_file} "
        input_str = input_str + f"{temp_dir} {max_mol}"
        pharmit_inputs.append(input_str)


    # write the job_list
    job_list_file: Path = (DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_list_file, "w") as f:
        for ind, pharmit_input in enumerate(pharmit_inputs):
            if ind:
                f.write("\n")
            f.write(pharmit_input)
    
    # create batch script to run slurm
    batch_script_file: Path = (DIR_SCRIPT / "run_pharmit_search.sh").resolve()
    with open(batch_script_file, "w") as f:
        f.write(f"sbatch --array=0-{len(pharmit_input_files)-1} --export=ALL pharm_search.slurm\n")




if __name__ == "__main__":
    # inputs
    disabled_pharmit_dir: Path = (DIR_STUDY / "031-validate-pharm-top-div" / "data" / "visual_inspect").resolve()
    pharmit_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "search_output").resolve()
    
    main(disabled_pharmit_dir, pharmit_output_dir, 2000)


