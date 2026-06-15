from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

HEADER: str = """#!/bin/bash
#SBATCH --job-name=get_pharms                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=128G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/batch.out                          # Output log path

module purge
module load pixi

"""


def main(top_div_set_dir: Path, output_dir: Path):
    """Will take in all the SDFs and auto generate a slurm script
    to extract all pharmacophores from them

    Args:
        top_div_set_dir (Path): location of top molecules for each
            region
        output_dir (Path): where the json list of pharmacophores
            will be output
    """
    slurm_str: str = HEADER

    # get all SDFs
    div_sdf_list: list[Path] = [item for item in top_div_set_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
    
    # create for every SDF
    for div_sdf in div_sdf_list:
        out_path: Path = (output_dir / f"{div_sdf.name.split(".")[0]}.out").resolve()
        line: str = f"pixi run -e pharmit pharmit pharma -in {str(div_sdf)} -out {str(out_path)}"
        slurm_str = slurm_str + "\n" + line

    slurm_path: Path = (DIR_SCRIPT / "get_pharms.slurm").resolve()
    with open(slurm_path, "w") as f:
        f.write(slurm_str)




if __name__ == "__main__":
    # inputs
    top_div_set_dir: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs").resolve()
    output_dir: Path = (DIR_STUDY / "028-pharms-top-div-set" / "data").resolve()

    main(top_div_set_dir, output_dir)


