
from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

def main(lig_inp_dir: Path, box_dirs: Path, pdb_dir: Path, output_dir: Path):
    """Will take in (1) ligands to dock (2) boxes to dock in (3) pdb to dock to.
    And create gnina inputs to dock every ligand to every box.

    Lig folder should have structure of: /region_#/mol#/group_#/output.sdf
    Boxes folder should have structure of: /box_#.txt
    PDB should just point to that file
    Output folder has structure of: /region_#/mol#/group_#.sdf
        Will create the output_dir if it does not exist

    Args:
        lig_inp_dir (Path): dir that holds are the ligands
        box_dirs (list[Path]): dir that holds all the boxes
        pdb_dir (Path): path of protein
        output_dir (Path): dir to store all outputs
    """
    
    # get all boxes
    box_list: list[Path] = [item for item in box_dirs.iterdir() if item.is_file()]

    gnina_inputs: list[str] = []
    # go through each region, get respective box
    region_dirs: list[Path] = [item for item in lig_inp_dir.iterdir() if item.is_dir() and item.name.startswith("region")]
    for region_dir in region_dirs:
        box_file: Path = [item for item in box_list if item.stem == region_dir.stem][0]
        region_name: str = region_dir.stem
        # go through each div set molecule
        mol_dirs: list[Path] = [item for item in region_dir.iterdir() if item.is_dir() and item.name.startswith("mol")]
        for mol_dir in mol_dirs:
            mol_name: str = mol_dir.stem
            # extract all setup molecules inside
            for sdf_file in mol_dir.rglob("gypsum_dl_success.sdf"):
                # create output file. Format output_dir/region_#/mol#/group_#.sdf
                output_file: Path = (output_dir / region_name / mol_name / f"{sdf_file.parent.stem}.sdf").resolve()
                if not output_file.parent.is_dir():
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                gnina_inputs.append(f"--receptor {pdb_dir} --ligand {sdf_file} --config {box_file} --out {output_file}")

    # write into file
    job_text: Path = Path(DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_text, "w") as f:
        f.write("\n".join(gnina_inputs))
    
    # edit run gnina slurm
    bash_script: Path = Path(DIR_SCRIPT / "run_gnina.sh").resolve()
    with open(bash_script, "w") as f:
        f.write(f"sbatch --array=0-{len(gnina_inputs)-1} --export=ALL dock.slurm\n")


if __name__ == "__main__":
    # imports
    lig_inp_dir = Path(DIR_STUDY / "041-setup-pharm-top-div-set" / "data" / "output_sdf").resolve()
    """The overall folder holding all setup ligands. Folder should have structure of:
    region_#/mol#/group_#/output.sdf"""
    box_dirs = Path(DIR_STUDY / "021-ftmap-box" / "data" / "box").resolve()
    """Folder that holds all the docking boxes. Should have all boxes stored in this directory
    in a .txt file."""
    pdb_dir = Path(DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb").resolve()
    """where the PDB is held"""
    output_dir = Path(DIR_STUDY / "051-dock-pharm-div-set" / "data" / "docked_compounds").resolve()
    """Where the docked compounds will be stored. WIll create files if they do not exist."""

    main(lig_inp_dir, box_dirs, pdb_dir, output_dir)





