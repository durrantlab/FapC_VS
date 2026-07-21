
from pathlib import Path


def main(
    sdf_input_dir: Path, split_sdf_dir: Path, split_size: int, 
    gypsum_sdf_dir: Path, DIR_SCRIPT: Path
):
    """Takes in all the SDF to be gypsumed, splits into X chunks, then creates
    gypsum inputs to be run

    Args:
        sdf_input_dir: where SDF inputs are held (searches for `<>.sdf` recursively)
        split_sdf_dir: where SDFs split into specific size are held
            Directory created if not already present.
            Will add <relative path of input>/mol_#/ directories to it
            If directories already exist, will skip splitting
        split_size: how many molecules are in each split
        gypsum_sdf_dir: where final gypsum outputs are held
            Directory created if not already present
            Will add <relative path of input>/mol_#/group_# directories to it
    """
    # get all input files
    sdf_input_files = [
            item
            for item in sdf_input_dir.rglob("*")
            if item.is_file() and item.suffix == ".sdf"
        ]

    args_list: list[str] = []
    # for each molecule
    for sdf_input_file in sdf_input_files:
        # path of input SDF relative to input path
        rel_path = sdf_input_file.relative_to(sdf_input_dir).parent
        # split into chunks
        mol_split_sdf_dir: Path = (
            split_sdf_dir / str(rel_path) / sdf_input_file.stem
        ).resolve()
        if not mol_split_sdf_dir.is_dir():
            mol_split_sdf_dir.mkdir(parents=True, exist_ok=True)
            sdf_list: list[Path] = sdf_set_size_split(
                sdf_input_file, mol_split_sdf_dir, split_size
            )
        else:
            sdf_list: list[Path] = [
                item
                for item in mol_split_sdf_dir.iterdir()
                if item.is_file() and item.suffix == ".sdf"
            ]
        # setup gypsum input for each file
        for sdf_file in sdf_list:
            mol_gypsum_sdf_dir: Path = (
                gypsum_sdf_dir
                / rel_path
                / sdf_input_file.stem
                / sdf_file.stem
            ).resolve()
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


def sdf_set_size_split(
    input_mol_file: Path, mol_split_sdf_dir: Path, split_size: int
) -> list[Path]:
    """Will take in a directory with SDFs and split them into new SDF files with
    exactly 'split_size' number of molecules in each. Last may be less.

    Args:
        input_mol_file: molecuel being split up
        mol_split_sdf_dir: directory where split molecules are put
        split_size: how many should be in each file

    Return:
        List of all SDF files created
    """

    # read in all the SDFs
    with open(input_mol_file, "r") as f:
        all_molecules: list[str] = [
            item.strip() for item in f.read().strip().split("$$$$")[:-1]
        ]
    # write out into chunks of split_size
    num_mols: int = len(all_molecules)
    all_sdfs: list[Path] = []
    for sdf_ind, start in enumerate(range(0, num_mols, split_size)):
        end = start + split_size  # end is not inclusive
        if end > num_mols:
            end = num_mols
        new_sdf: str = "\n\n$$$$\n".join(all_molecules[start:end]) + "\n\n$$$$"
        sdf_file: Path = Path(mol_split_sdf_dir / f"group_{sdf_ind}.sdf")
        with open(sdf_file, "w") as f:
            f.write(new_sdf)
        all_sdfs.append(sdf_file)
    return all_sdfs
