import math
from pathlib import Path

from FapC_VS.gnina.create_jobs import create_n_sdf

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


if __name__ == "__main__":
    # inputs
    lig_inp_dir: Path = Path(
        "/ihome/jdurrant/nag81/PSMa1/Initial_Dock/Gypsum_Files"
    ).resolve()
    lig_op_dir: Path = Path(DIR_SCRIPT / ".." / "data" / "concat_lig").resolve()

    create_n_sdf.main(lig_inp_dir, lig_op_dir, 30)
