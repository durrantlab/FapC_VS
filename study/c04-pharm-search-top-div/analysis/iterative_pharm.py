import argparse
from pathlib import Path

from FapC_VS.pharmit import iterative_pharm
from FapC_VS.pharmit import iterative_pharm_args

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


if __name__ == "__main__":

    # default params
    region: str = "region_1"
    mol_num: str = "8"
    args = iterative_pharm_args.main(DIR_STUDY, DIR_SCRIPT, region, mol_num)
    
    iterative_pharm.main(
        Path(args.pharm_list_file),
        Path(args.sdf_file),
        Path(args.csv_file),
        Path(args.temp_dir),
        args.max_mol,
    )
