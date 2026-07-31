from pathlib import Path

from FapC_VS.gnina import check_gnina_output

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


if __name__ == "__main__":
    gnina_input_dir: Path = (DIR_SCRIPT / ".." / "data" / "cleaned_compounds").resolve()
    gnina_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "docked_compounds").resolve()
    check_gnina_output.main(gnina_input_dir, gnina_output_dir, FILE_LOG)
