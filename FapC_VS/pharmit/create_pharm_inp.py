
from pathlib import Path

HEADER: str = """#!/bin/bash
#SBATCH --job-name=get_pharms                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=128G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=batch.out                          # Output log path

module purge
module load pixi

"""


def main(sdf_dir: Path, output_dir: Path, DIR_SCRIPT: Path):
    """Will take in all SDFs in the path and auto generate a slurm script
    to extract all pharmacophores from them

    Args:
        sdf_dir: folder that holds all the SDFs. 
            Does not check rrecursively.
        output_dir: where the json list of pharmacophores
            will be output
    """
    slurm_str: str = HEADER

    # get all SDFs
    div_sdf_list: list[Path] = [
        item
        for item in sdf_dir.iterdir()
        if item.is_file() and item.suffix == ".sdf"
    ]

    # create for every SDF
    for div_sdf in div_sdf_list:
        out_path: Path = (output_dir / f"{div_sdf.name.split('.')[0]}.json").resolve()
        line: str = (
            f"pixi run -e pharmit pharmit pharma -in {str(div_sdf)} -out {str(out_path)}"
        )
        slurm_str = slurm_str + "\n" + line

    slurm_path: Path = (DIR_SCRIPT / "get_pharms.slurm").resolve()
    with open(slurm_path, "w") as f:
        f.write(slurm_str)
