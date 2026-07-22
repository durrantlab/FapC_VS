
from pathlib import Path
from FapC_VS.gnina.clean_up_gypsum import clean_up_sdf


def main(
    lig_inp_dir: Path,
    box_dirs: Path,
    pdb_dir: Path,
    cleaned_dir: Path,
    output_dir: Path,
    DIR_SCRIPT: Path
):
    """Will take in (1) ligands to dock (2) boxes to dock in (3) pdb to dock to.
    And create gnina inputs to dock every ligand to every box.

    Lig folder should have structure of: /region_#/mol#/group_#/output.sdf
    Boxes folder should have structure of: /box_#.txt
    PDB should just point to that file
    Cleaned folder has structure of: /region_#/mol#/group_#.sdf
        Will create the cleaned_dir if it does not exist
        Just removes empty settings molecule at top
        Only creates if cleaned .sdf does not exist
    Output folder has structure of: /region_#/mol#/group_#.sdf
        Will create the output_dir if it does not exist
        Only creates if gnina OP .sdf does not exist

    Args:
        lig_inp_dir: dir that holds are the ligands
        box_dirs (list[Path]): dir that holds all the boxes
        pdb_dir: path of protein
        cleaned_dir: dir to store output of gypsum op cleaning
        output_dir: dir to store all outputs
    """

    # get all boxes
    box_list: list[Path] = [item for item in box_dirs.iterdir() if item.is_file()]

    gnina_inputs: list[str] = []
    # go through each region, get respective box
    region_dirs: list[Path] = [
        item
        for item in lig_inp_dir.iterdir()
        if item.is_dir() and item.name.startswith("region")
    ]
    for region_dir in region_dirs:
        box_file: Path = [item for item in box_list if item.stem == region_dir.stem][0]
        region_name: str = region_dir.stem
        # go through each div set molecule
        mol_dirs: list[Path] = [
            item
            for item in region_dir.iterdir()
            if item.is_dir() and item.name.startswith("mol")
        ]
        for mol_dir in mol_dirs:
            mol_name: str = mol_dir.stem
            # extract all setup molecules inside
            for sdf_file in mol_dir.rglob("gypsum_dl_success.sdf"):
                # clean up SDFs and write them out
                clean_sdf_file: Path = (
                    cleaned_dir / region_name / mol_name / f"{sdf_file.parent.stem}.sdf"
                ).resolve()
                if not clean_sdf_file.exists():
                    if not clean_sdf_file.parent.is_dir():
                        clean_sdf_file.parent.mkdir(parents=True, exist_ok=True)
                    settings: str = clean_up_sdf(sdf_file, clean_sdf_file)
                    settings_file: Path = (
                        cleaned_dir / "gypsum_settings.sdf"
                    ).resolve()
                    if not settings_file.exists():
                        with open(settings_file, "w") as f:
                            f.write(settings)

                # create output file. Format output_dir/region_#/mol#/group_#.sdf. Will NOT run if sdf already exists. make sure to clear before
                output_file: Path = (
                    output_dir / region_name / mol_name / f"{sdf_file.parent.stem}.sdf"
                ).resolve()
                if not output_file.exists():
                    if not output_file.parent.is_dir():
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                    gnina_inputs.append(
                        f"--receptor {pdb_dir} --ligand {clean_sdf_file} --config {box_file} --out {output_file}"
                    )

    # write into file
    job_text: Path = Path(DIR_SCRIPT / "job_list.txt").resolve()
    with open(job_text, "w") as f:
        f.write("\n".join(gnina_inputs))

    # edit run gnina slurm
    bash_script: Path = Path(DIR_SCRIPT / "run_gnina.sh").resolve()
    with open(bash_script, "w") as f:
        f.write(f"sbatch --array=0-{len(gnina_inputs)-1} --export=ALL dock.slurm\n")
