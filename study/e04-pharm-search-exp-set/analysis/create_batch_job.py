import shutil
import sys
from pathlib import Path
from FapC_VS.pharmit import create_batch_iterative_pharm_job

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


def main(
    main_disabled_pharmit_dir: Path,
    main_pharmit_output_dir: Path,
    pharm_search_base: Path,
    iterative_pharm_loc: Path,
    max_ret_mol: int = 2000,
    DIR_SCRIPT: Path = DIR_SCRIPT,
):
    """Will take in pharmits input files and create a slurm to run the iterative pharm script.

    On running pharmit, for each molecule in each region, will find up to 2000 similar molecules, store them in
    a csv (name is [molecule name].csv) and in an sdf as well (same name, but .sdf)

    Args:
        disabled_pharmit_dir: where the inputs with disabled pharms based
            on prolif are stored. Should just have jsons inside
        pharmit_output_dir: where final pharmit search inputs will be stored
            will be placed into folders named after name of csv/sdf
            will be named after molecule
        pharm_search_base: path to file with the basis for the .slurm file
        iterative_pharm_loc: path to iterative_pharmit.py script
        max_ret_mol: max number of molecules to be returned per molecule
    """

    # read in disabled pharmits
    pharmit_input_jsons: list[Path] = [
        item
        for item in main_disabled_pharmit_dir.iterdir()
        if item.is_file() and item.suffix == ".json"
    ]

    # create the python inputs
    pharmit_inputs: list[str] = []
    for pharmit_json in pharmit_input_jsons:
        # setup inputs
        mol_name: str = pharmit_json.stem.split("_")[0]

        pharm_list_file: Path = pharmit_json
        sdf_file: Path = (main_pharmit_output_dir / f"{mol_name}.sdf").resolve()
        csv_file: Path = (main_pharmit_output_dir / f"{mol_name}.csv").resolve()
        temp_dir: Path = DIR_SCRIPT / "temp" / mol_name
        max_mol: int = max_ret_mol

        # OP directories are automatically created by iterative_pharmit, so not made here

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
            f"sbatch --array=0-{len(pharmit_input_jsons)-1} --export=ALL pharm_search.slurm\n"
        )

    # create the slurm to go to correct python
    with open(pharm_search_base, "r") as f:
        slurm_text: list[str] = f.read().strip().split("\n")
    slurm_text[23] = (
        f'pixi run python -u {str(iterative_pharm_loc)} $ARGS" | tee "$LOG'
    )
    pharm_slurm_file: Path = (pharm_search_base.parent / "pharm_search.slurm").resolve()
    with open(pharm_slurm_file, "w") as f:
        f.write("\n".join(slurm_text))


if __name__ == "__main__":
    # inputs
    disabled_pharmit_dir: Path = (
        DIR_STUDY / "e03-validate-pharm-exp" / "data" / "visual_inspect"
    ).resolve()
    pharmit_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "search_output").resolve()
    pharm_search_base: Path = (DIR_SCRIPT / "pharm_search_BASE.slurm").resolve()
    iterative_pharm_loc: Path = (
        DIR_STUDY / "c04-pharm-search-top-div" / "analysis" / "iterative_pharm.py"
    ).resolve()

    create_batch_iterative_pharm_job.main(
        disabled_pharmit_dir,
        pharmit_output_dir,
        pharm_search_base,
        5000,
    )
