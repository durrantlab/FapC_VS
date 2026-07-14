from typing import Any

import sys
import warnings

from pandas.core.frame import DataFrame

with warnings.catch_warnings(record=True):
    from pathlib import Path

    import prolif as plf
    from rdkit import Chem

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()

# add the directory of script to path
sys.path.insert(0, str((DIR_STUDY / "027-key-top-div-inter" / "analysis").resolve()))
import find_interacts

if __name__ == "__main__":
    # inputs
    exp_ligands_dir: Path = (DIR_STUDY / "026-compare-sets" / "data").resolve()
    protein_file: Path = (
        DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb"
    ).resolve()
    op_dir: Path = (DIR_STUDY / "062-key-exp-inter" / "data").resolve()
    find_interacts.main(exp_ligands_dir, protein_file, op_dir)
