
from pathlib import Path

def clean_up_sdf(sdf_file: Path, op_file: Path) -> str:
    with open(sdf_file, "r") as f:
        mols: list[str] = [item.strip() for item in f.read().strip().split("$$$$")]
    with open(op_file, "w") as f:
        f.write("\n\n$$$$\n".join(mols[1:]))
    return mols[0]

