from pathlib import Path
import sys


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()

sys.path.insert(0, str((DIR_STUDY / "031-validate-pharm-top-div").resolve()))
from analysis.lib import load_concatenated_json


def main(disabled_pharmit_dir: Path, pharmit_output_dir: Path, min_pharm: int = 3):
    """Will take in pharmits with disabled pharms and create inputs
    for pharmit with variety of different pharmacophores enabled 
    / disabled

    Args:
        disabled_pharmit_dir (Path): where the inputs with disabled pharms based
            on prolif are stored
        pharmit_output_dir (Path): where final pharmit search inputs will be stored
            All inputs for 1 region will be in a file together
    """
    
    # read in disabled pharmits
    pharm_list: list[Path] = [item for item in disabled_pharmit_dir.iterdir() if item.is_file() and item.suffix == ".json"]
    regions: list[str] = []
    pharm_dict: dict[str, list[dict]] = {}
    for pharm_json in pharm_list:
        region: str = "_".join(pharm_json.name.split(".")[0].split("_")[0:2])
        regions.append(region)
    
    






if __name__ == "__main__":
    # inputs
    disabled_pharmit_dir: Path = (DIR_SCRIPT / "031-validate-pharm-top-div" / "disabled_pharms_input").resolve()
    pharmit_output_dir: Path = (DIR_STUDY / ".." / "data" / "pharmit_inputs").resolve()
    
    main(disabled_pharmit_dir, pharmit_output_dir)


