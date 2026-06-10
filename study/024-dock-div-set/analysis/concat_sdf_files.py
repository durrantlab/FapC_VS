from pathlib import Path
import math

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


def main(lig_inp_dir: Path, lig_op_dir: Path, n_sdf: int):
    """Will take in a list of ligands and combine into
    n_sdf number of sdf files. Number of SDF files should
    be how many total jobs will be run

    Args:
        lig_inp_dir (Path): Where ligands by themselves are found
        lig_op_dir (Path): Where ligands together will be placed
        n_sdf (int): number of together SDF files to be made
    """
    if not lig_op_dir.parent.is_dir():
        lig_op_dir.parent.mkdir(parents=True, exist_ok=True)

    lig_list: list[Path] = [item for item in lig_inp_dir.iterdir() if item.is_file()]
    lig_num: float = len(lig_list)

    # not enough sdfs
    if lig_num < n_sdf:
        raise Exception("Not enough SDFs, decrease n_sdf")

    # determine count in each SDF
    count_per_sdf: int = math.ceil(lig_num / n_sdf)

    min: int = 0
    max: int = count_per_sdf
    
    # for each new file
    for file_num in range(0, n_sdf):
        file_path: Path = Path(lig_op_dir / f"ligs_{file_num:03d}.sdf").resolve()
        # go through correct range and get all files
        if max >= len(lig_list):
            max = len(lig_list) - 1
        
        if min >= len(lig_list):
            raise Exception("Somehow min messed up")

        towrite: str = ""
        for file_ind in range(min, max+1):
            with open(lig_list[file_ind], "r") as f:
                towrite = towrite + f.read() + "\n"

        min = max + 1
        max = max + count_per_sdf

        with open(file_path, "w") as f:
            f.write(towrite)





if __name__ == "__main__":
    # inputs
    lig_inp_dir: Path = Path("/ihome/jdurrant/nag81/PSMa1/Initial_Dock/Gypsum_Files").resolve()
    lig_op_dir: Path = Path(DIR_SCRIPT / ".." / "data" / "concat_lig").resolve()
    
    main(lig_inp_dir, lig_op_dir, 30)


