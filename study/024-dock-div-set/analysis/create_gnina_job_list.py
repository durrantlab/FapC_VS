
from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

def main(lig_inp_dir: Path, box_dirs: Path, pdb_dir: Path, output_dir: Path):
    """Will take in (1) ligands to dock (2) boxes to dock in (3) pdb to dock to
    (4) where to store docked residues / there scores (?)

    Args:
        lig_inp_dir (Path): dir that holds are the ligands
        box_dirs (list[Path]): dir that holds all the boxes
        pdb_dir (Path): path of protein
        output_dir (Path): dir to store all outputs
    """
    
    # get all ligands, boxes
    lig_list: list[Path] = [item for item in lig_inp_dir.iterdir() if item.is_file()]
    box_list: list[Path] = [item for item in box_dirs.iterdir() if item.is_file()]

    gnina_inputs = []
    # for every box and ligand, create an input
    for box in box_list:
        for lig in lig_list:
            # --receptor $receptor --ligand $LIGAND_FILE --config $config --out $OUT
            out: Path = Path(output_dir / f"{box.name.split(".")[0]}" / f"{lig.name.split(".")[0].split("__")[1]}.sdf").resolve()
            gnina_inputs.append(f"--receptor {pdb_dir} --ligand {lig} --config {box} --out {out}")
            if not out.parent.is_dir():
                out.parent.mkdir(parents=True, exist_ok=True)

    
    # write into file
    job_text: Path = Path(DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_text, "w") as f:
        for line in gnina_inputs:
            f.write(line + "\n")
    
    # edit run gnina slurm
    with open("run_gnina.sh", "w") as f:
        min = -1
        for max in range(0, len(gnina_inputs)-1, 499)[1:]:
            f.write(f"sbatch --array={min+1}-{max} --export=ALL dock.slurm\n")
            min = max
        if min != len(gnina_inputs)-1:
            f.write(f"sbatch --array={min+1}-{len(gnina_inputs)-1} --export=ALL dock.slurm")



if __name__ == "__main__":
    # imports
    lig_inp_dir = Path("/ihome/jdurrant/nag81/PSMa1/Initial_Dock/Gypsum_Files").resolve()
    box_dirs = Path(DIR_STUDY / "021-ftmap-box" / "data" / "box").resolve()
    pdb_dir = Path(DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb").resolve()
    output_dir = Path(DIR_STUDY / "024-dock-div-set" / "data" / "docked_compounds").resolve()

    main(lig_inp_dir, box_dirs, pdb_dir, output_dir)





