from pathlib import Path
from FapC_VS.gnina.create_jobs import lig_each_box

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # imports
    lig_inp_dir = Path(DIR_STUDY / "b02-dock-div-set" / "data" / "concat_lig").resolve()
    box_dirs = Path(DIR_STUDY / "a02-ftmap-box" / "data" / "box").resolve()
    pdb_dir = Path(
        DIR_STUDY / "b01-prep-protein-dock" / "data" / "9nqd_protonated.pdb"
    ).resolve()
    output_dir = Path(
        DIR_STUDY / "b02-dock-div-set" / "data" / "docked_compounds"
    ).resolve()

    lig_each_box.main(lig_inp_dir, box_dirs, pdb_dir, output_dir)
