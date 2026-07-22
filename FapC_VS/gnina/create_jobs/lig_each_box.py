from pathlib import Path


def main(lig_inp_dir: Path, box_dirs: Path, 
         pdb_dir: Path, output_dir: Path, DIR_SCRIPT: Path):
    """Will take in (1) ligands to dock (2) boxes to dock in (3) pdb to dock to.
    And create gnina inputs to dock every ligand to every box.

    Args:
        lig_inp_dir: dir that holds are the ligands
        box_dirs (list[Path]): dir that holds all the boxes
        pdb_dir: path of protein
        output_dir: dir to store all outputs
    """

    # get all ligands, boxes
    lig_list: list[Path] = [item for item in lig_inp_dir.iterdir() if item.is_file()]
    box_list: list[Path] = [item for item in box_dirs.iterdir() if item.is_file()]

    gnina_inputs = []
    # for every box and ligand, create an input
    for box in box_list:
        for lig in lig_list:
            # --receptor $receptor --ligand $LIGAND_FILE --config $config --out $OUT
            out: Path = Path(
                output_dir
                / f"{box.name.split('.')[0]}"
                / f"{lig.name.split('.')[0]}.sdf"
            ).resolve()
            gnina_inputs.append(
                f"--receptor {pdb_dir} --ligand {lig} --config {box} --out {out}"
            )
            if not out.parent.is_dir():
                out.parent.mkdir(parents=True, exist_ok=True)

    # write into file
    job_text: Path = Path(DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_text, "w") as f:
        for line in gnina_inputs:
            f.write(line + "\n")

    # edit run gnina slurm
    with open((DIR_SCRIPT / "run_gnina.sh"), "w") as f:
        f.write(f"sbatch --array=0-{len(gnina_inputs)-1} --export=ALL dock.slurm\n")
