import argparse
from pathlib import Path

def main(DIR_STUDY: Path, DIR_SCRIPT: Path, 
         region_def: str, mol_num_def: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="runs pharmit iteratively on a pharmacophore list"
    )
    pharm_list_file: Path = (
        DIR_STUDY
        / "c03-validate-pharm-top-div"
        / "data"
        / region_def
        / f"mol{mol_num_def}_input.json"
    ).resolve()
    """The location of the pharmit sesquarch input (pharmacophore list) that is
    being searched. Will be input via command line"""
    parser.add_argument(
        "pharm_list_file",
        default=pharm_list_file,
        nargs="?",
        help="where pharmacophore json is located",
    )

    sdf_file: str = str(
        (
            DIR_SCRIPT / ".." / "data" / "search_output" / 
            region_def / f"mol{mol_num_def}.sdf"
        ).resolve()
    )
    """where the SDF file from pharmit search will be stored"""
    parser.add_argument(
        "sdf_file",
        default=sdf_file,
        nargs="?",
        help="where the SDF file from pharmit search will be stored",
    )

    csv_file: str = str(
        (
            DIR_SCRIPT / ".." / "data" / "search_output" / 
            region_def / f"mol{mol_num_def}.csv"
        ).resolve()
    )
    """where the CSV file from pharmit search will be stored"""
    parser.add_argument(
        "csv_file",
        default=csv_file,
        nargs="?",
        help="where the CSV file from pharmit search will be stored",
    )

    temp_dir: str = str(
        (DIR_SCRIPT / "temp" / region_def / f"mol{mol_num_def}").resolve()
    )
    """where temporary files will be stored. Each parallel run should be unique"""
    parser.add_argument(
        "temp_dir",
        default=temp_dir,
        nargs="?",
        help="where temporary files will be stored. Each parallel run should be unique",
    )

    max_mol: int = 2000
    """the max number of results for a molecule"""
    parser.add_argument(
        "max_mol",
        default=max_mol,
        type=int,
        nargs="?",
        help="the max number of results for a molecule",
    )

    return parser.parse_args()
