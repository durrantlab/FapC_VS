from pathlib import Path
import sys


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

sys.path.insert(0, str((DIR_STUDY / "031-validate-pharm-top-div").resolve()))


def main(disabled_pharmit_dir: Path, pharmit_output_dir: Path, min_pharm: int = 2000):
    """Will take in pharmits input files and create a slurm to run pharmit with
    them

    Args:
        disabled_pharmit_dir (Path): where the inputs with disabled pharms based
            on prolif are stored
        pharmit_output_dir (Path): where final pharmit search inputs will be stored
            All inputs for 1 region will be in a file together
    """
    
    # read in disabled pharmits
    pharmit_inp_region_dirs: list[Path] = [item for item in disabled_pharmit_dir.iterdir() if item.is_dir() and item.name.startswith("region")]
    regions: list[str] = []
    pharmit_input_files = []
    for pharmit_inp_dir in pharmit_inp_region_dirs:
        region: str = pharmit_inp_dir.name
        regions.append(region)
        pharmit_input_files.extend([item for item in pharmit_inp_dir.iterdir() if item.is_file() and item.suffix == ".json"])

    # create the pharmit inputs
    pharmit_inputs: list[str] = []
    for pharmit_json in pharmit_input_files:
        output_name: str = pharmit_json.name.split(".")[0]
        output_sdf: Path = (pharmit_output_dir / pharmit_json.parent.name / f"{output_name}.sdf")
        output_txt: Path = (pharmit_output_dir / pharmit_json.parent.name / f"{output_name}.txt")
        if not output_sdf.parent.is_dir():
            output_sdf.parent.mkdir(parents=True, exist_ok=True)
        pharmit_inputs.append(f"-in {pharmit_json} -out {output_sdf} {output_txt} -max-hit {min_pharm}")

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
    disabled_pharmit_dir: Path = (DIR_STUDY / "031-validate-pharm-top-div" / "data").resolve()
    pharmit_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "search_output").resolve()
    
    main(disabled_pharmit_dir, pharmit_output_dir, 2000)


