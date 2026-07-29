
import shutil
import sys
from pathlib import Path


def main(
    main_disabled_pharmit_dir: Path,
    main_pharmit_output_dir: Path,
    DIR_SCRIPT: Path,
    max_ret_mol: int = 2000,
) -> None:
    """Will take in pharmits input files and create a slurm to run 
    the iterative pharm script.

    On running pharmit, for each pharmacophore JSON in the directory 
    (searches recursively), will find up to <max_ret_mol> similar molecules, s
    tore them in a csv (name is <main_pharmit_output_dir>/<file path in input>/
    <molecule name>.csv) and in an sdf as well (same name, but .sdf)

    Args:
        disabled_pharmit_dir: where the inputs with disabled pharms based
            on prolif are stored. Has jsons for each molecule inside
            Expects the input files to have format: mol#_input.json
            Searches recursively through folder
        pharmit_output_dir: where final pharmit search inputs will be stored
            folder stored in is same as file (if exist) in input
            name of csv/sdf will be named after molecule
        DIR_SCRIPT: directory of the script calling this function
            Temporary files and files to run iterative_pharmit will be placed here
        max_ret_mol: max number of molecules to be returned per molecule
    """

    # read in disabled pharmits
    pharmit_input_files = [
            item
            for item in main_disabled_pharmit_dir.rglob("*")
            if item.is_file() and item.suffix == ".json"
        ]

    # create the python inputs
    pharmit_inputs: list[str] = []
    for pharmit_json in pharmit_input_files:
        # setup inputs
        mol_name: str = pharmit_json.stem.split("_")[0]
        rel_path = pharmit_json.relative_to(main_disabled_pharmit_dir).parent

        pharm_list_file: Path = pharmit_json
        sdf_file: Path = (
            main_pharmit_output_dir / str(rel_path) / f"{mol_name}.sdf"
        ).resolve()
        csv_file: Path = (
            main_pharmit_output_dir / str(rel_path) / f"{mol_name}.csv"
        ).resolve()
        temp_dir: Path = DIR_SCRIPT / "temp" / str(rel_path) / mol_name
        max_mol: int = max_ret_mol

        # OP directories are automatically created by iterative_pharmit, 
        # so not made here

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
        f.write(
            f"sbatch --array=0-{len(pharmit_input_files)-1} --export=ALL pharm_search.slurm\n"
        )
