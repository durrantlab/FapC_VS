
import argparse
from pathlib import Path
from FapC_VS.pharmit import pharmit_server_query

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


if __name__ == "__main__":
    query_path: Path = (
        DIR_STUDY
        / "c03-validate-pharm-top-div"
        / "data"
        / "region_1"
        / "reg_1_mol1_base_input.json"
    ).resolve()
    out_path: Path = (
        DIR_SCRIPT / ".." / "data" / "search_output" / "region_1" / "mol1" / "op.sdf"
    ).resolve()
    interval: float = 16.0
    timeout: float = 600.0
    pharmit_server_query.run(query_path, out_path, interval, timeout, None, 2000, FILE_LOG)
