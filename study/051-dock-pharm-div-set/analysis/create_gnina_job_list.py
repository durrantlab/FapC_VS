
from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

def main(lig_inp_dir: Path, box_dirs: Path, pdb_dir: Path, cleaned_dir: Path, output_dir: Path):
    """Will take in (1) ligands to dock (2) boxes to dock in (3) pdb to dock to.
    And create gnina inputs to dock every ligand to every box.

    Lig folder should have structure of: /region_#/mol#/group_#/output.sdf
    Boxes folder should have structure of: /box_#.txt
    PDB should just point to that file
    Cleaned folder has structure of: /region_#/mol#/group_#.sdf
        Will create the cleaned_dir if it does not exist
        Just removes empty settings molecule at top
    Output folder has structure of: /region_#/mol#/group_#.sdf
        Will create the output_dir if it does not exist

    Args:
        lig_inp_dir (Path): dir that holds are the ligands
        box_dirs (list[Path]): dir that holds all the boxes
        pdb_dir (Path): path of protein
        cleaned_dir (Path): dir to store output of gypsum op cleaning
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
                # clean up SDFs and write them out
                clean_sdf_file: Path = (cleaned_dir / region_name / mol_name / f"{sdf_file.parent.stem}.sdf").resolve()
                if not clean_sdf_file.exists():
                    if not clean_sdf_file.parent.is_dir():
                        clean_sdf_file.parent.mkdir(parents=True, exist_ok=True)
                    settings: str = clean_up_sdf(sdf_file, clean_sdf_file)
                    settings_file: Path = (cleaned_dir / "gypsum_settings.sdf").resolve()
                    if not settings_file.exists():
                        with open(settings_file, "w") as f:
                            f.write(settings)

                # create output file. Format output_dir/region_#/mol#/group_#.sdf
                output_file: Path = (output_dir / region_name / mol_name / f"{sdf_file.parent.stem}.sdf").resolve()
                if not output_file.parent.is_dir():
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                gnina_inputs.append(f"--receptor {pdb_dir} --ligand {clean_sdf_file} --config {box_file} --out {output_file}")

    # write into file
    job_text: Path = Path(DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_text, "w") as f:
        f.write("\n".join(gnina_inputs))
    
    # edit run gnina slurm
    bash_script: Path = Path(DIR_SCRIPT / "run_gnina.sh").resolve()
    with open(bash_script, "w") as f:
        f.write(f"sbatch --array=0-{len(gnina_inputs)-1} --export=ALL dock.slurm\n")



def clean_up_sdf(sdf_file: Path, op_file: Path) -> str:
    # NOTE: ran incorrectly initially, overwritting original files and adding in new issue,
    # so temporarily rewrote section to fix that. This is that. Below is script to
    # use normally
    with open(sdf_file, "r") as f:
        mols: list[str] = [item.strip() for item in f.read().strip().split("$$$$")]
    with open(op_file, "w") as f:
        f.write("\n\n$$$$\n".join(mols[:-1]))
    return mols[0]

"""def clean_up_sdf(sdf_file: Path, op_file: Path) -> str:
    # NOTE: ran incorrectly initially, overwritting original files and adding in new issue,
    # so temporarily rewrote section to fix that
    with open(sdf_file, "r") as f:
        mols: list[str] = [item.strip() for item in f.read().strip().split("$$$$")]
    with open(op_file, "w") as f:
        f.write("\n\n$$$$\n".join(mols)[:-1])
    return mols[0]"""

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
    cleaned_dir = Path(DIR_STUDY / "051-dock-pharm-div-set" / "data" / "cleaned_compounds").resolve()
    """Where the cleaned compounds will be stored. WIll create files if they do not exist."""
    output_dir = Path(DIR_STUDY / "051-dock-pharm-div-set" / "data" / "docked_compounds").resolve()
    """Where the docked compounds will be stored. WIll create files if they do not exist."""

    main(lig_inp_dir, box_dirs, pdb_dir, cleaned_dir, output_dir)





