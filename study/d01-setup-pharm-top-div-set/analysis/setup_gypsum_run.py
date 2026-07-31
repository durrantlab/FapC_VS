from pathlib import Path

from FapC_VS.gnina import setup_gypsum_run

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    sdf_input_dir: Path = (
        DIR_STUDY / "c04-pharm-search-top-div" / "data" / "search_output"
    )
    """Where input SDFs are. Will search recursively through iles for all .sdfs"""
    split_sdf_dir: Path = DIR_SCRIPT / ".." / "data" / "split_sdf"
    """Where split SDFs to prepare for gypsum are held"""
    gypsum_sdf_dir: Path = DIR_SCRIPT / ".." / "data" / "output_sdf"
    """Where the outputs of gypsum are held"""

    setup_gypsum_run.main(sdf_input_dir, split_sdf_dir, 250, gypsum_sdf_dir, DIR_SCRIPT)
