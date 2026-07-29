
from pathlib import Path

def clean_up_sdf(sdf_file: Path, op_file: Path) -> str:
    """Take in an SDF file output from gypsum, remove the first molecule (which
    is just settings), write the rest into op_file, and then return the settings
    as a string

    Args:
        sdf_file: SDF file output from gypsum  
        op_file: where the edited SDF file will be placed

    Returns:
        the gypsum settings that were removed
    """
    with open(sdf_file, "r") as f:
        mols: list[str] = [item.strip() for item in f.read().strip().split("$$$$")]
    with open(op_file, "w") as f:
        f.write("\n\n$$$$\n".join(mols[1:]))
    return mols[0]

