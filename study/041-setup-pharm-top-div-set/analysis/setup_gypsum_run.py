from pathlib import Path
import logging


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


def main(sdf_input_dir: Path, split_sdf_dir: Path, split_size: int, gypsum_sdf_dir: Path):
    """Takes in all the SDF to be gypsumed, splits into X chunks, then creates
    gypsum inputs to be run

    Args:
        sdf_input_dir (Path): where SDF inputs are held (organized region_#/mol#)
        split_sdf_dir (Path): where SDFs split into specific size are held
        split_size (Path): how many molecules are in each split
        gypsum_sdf_dir (Path): where final gypsum outputs are held
    """
    # for each molecule:
    input_region_dirs: list[Path] = [item for item in sdf_input_dir.iterdir() if item.is_dir() and item.name.startswith("region")]
    args_list: list[str] = []
    for input_region_dir in input_region_dirs:
        input_mol_dirs = [item for item in input_region_dir.iterdir() if item.is_dir() and item.name.startswith("mol")]
        for input_mol_dir in input_mol_dirs:
            # split into chunks
            mol_split_sdf_dir: Path = (split_sdf_dir / input_region_dir.name / input_mol_dir.name).resolve()
            if not mol_split_sdf_dir.is_dir():
                mol_split_sdf_dir.mkdir(parents=True, exist_ok=True)
            sdf_list: list[Path] = sdf_set_size_split(input_mol_dir, mol_split_sdf_dir, split_size)
            # setup gypsum input for each file
            for sdf_file in sdf_list:
                mol_gypsum_sdf_file: Path = (gypsum_sdf_dir / input_region_dir.name / input_mol_dir.name / sdf_file.name).resolve()
                args: str = f"-s {sdf_file} -o {mol_gypsum_sdf_file}"
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
        f.write(f"sbatch --array=0-{len(arg)-1} --export=ALL run_gypsum.slurm\n")


def sdf_set_size_split(input_mol_dir: Path, mol_split_sdf_dir: Path, 
                       split_size: int) -> list[Path]:
    """Will take in a directory with SDFs and split them into new SDF files with
    exactly 'split_size' number of molecules in each. Last may be less.

    Args:
        input_mol_dir (Path): directory where molecules are held
        mol_split_sdf_dir (Path): directory where split molecules are put
        split_size (int): how many should be in each file
    
    Return:
        List of all SDF files created 
    """

    # read in all the SDFs
    input_sdfs: list[Path] = [item for item in input_mol_dir.iterdir() if item.is_file() and item.name.endswith(".sdf")]
    all_molecules: list[str] = []
    for input_sdf in input_sdfs:
        with open(input_sdf, "r") as f:
            file_mols: list[str] = [item.strip() for item in f.read().strip().split("$$$$")[:-1]]
            all_molecules.extend(file_mols)
    # write out into chunks of split_size
    num_mols: int = len(all_molecules)
    all_sdfs: list[Path] = []
    for sdf_ind, start in enumerate(range(0, num_mols, split_size)):
        end = start + split_size # end is not inclusive
        if end > num_mols:
            end = num_mols
        new_sdf: str = "\n$$$$\n".join(all_molecules[start:end]) +"\n$$$$"
        sdf_file: Path = Path(mol_split_sdf_dir / f"group_{sdf_ind}.sdf")
        with open(sdf_file, "w") as f:
            f.write(new_sdf)
        all_sdfs.append(sdf_file)
    return all_sdfs


if __name__ == "__main__":
    # inputs
    sdf_input_dir: Path = (DIR_STUDY / "033-pharm-search-top-div" / "data" / "search_output")
    """Where input SDFs are. Will search recursively through iles for all .sdfs"""
    split_sdf_dir: Path = (DIR_SCRIPT / ".." / "data" / "split_sdf")
    """Where split SDFs to prepare for gypsum are held"""
    gypsum_sdf_dir: Path = (DIR_SCRIPT / ".." / "data" / "output_sdf")
    """Where the outputs of gypsum are held"""
    
    main(sdf_input_dir, split_sdf_dir, 250, gypsum_sdf_dir)


