from pathlib import Path

from FapC_VS.gnina.clean_up_gypsum import clean_up_sdf
from FapC_VS.gnina.create_jobs import lig_prev_box

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # imports
    lig_inp_dir = Path(
        DIR_STUDY / "d01-setup-pharm-top-div-set" / "data" / "output_sdf"
    ).resolve()
    """The overall folder holding all setup ligands. Folder should have structure of:
    region_#/mol#/group_#/output.sdf"""
    box_dirs = Path(DIR_STUDY / "a02-ftmap-box" / "data" / "box").resolve()
    """Folder that holds all the docking boxes. Should have all boxes stored in this directory
    in a .txt file."""
    pdb_dir = Path(
        DIR_STUDY / "b01-prep-protein-dock" / "data" / "9nqd_protonated.pdb"
    ).resolve()
    """where the PDB is held"""
    cleaned_dir = Path(
        DIR_STUDY / "d02-dock-pharm-div-set" / "data" / "cleaned_compounds"
    ).resolve()
    """Where the cleaned compounds will be stored. WIll create files if they do not exist."""
    output_dir = Path(
        DIR_STUDY / "d02-dock-pharm-div-set" / "data" / "docked_compounds"
    ).resolve()
    """Where the docked compounds will be stored. WIll create files if they do not exist."""

    lig_prev_box.main(
        lig_inp_dir, box_dirs, pdb_dir, cleaned_dir, output_dir, DIR_SCRIPT
    )
