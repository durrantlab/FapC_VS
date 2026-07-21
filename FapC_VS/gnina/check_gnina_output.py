
from pathlib import Path
import logging
from FapC_VS import enable_logging


def main(gnina_input_dir: Path, gnina_output_dir: Path, FILE_LOG: Path):
    # setup logging
    enable_logging(FILE_LOG)
    # extract all inputs
    for inp_path in Path(gnina_input_dir).rglob("group*.sdf"):
        lower_path: Path = inp_path.relative_to(gnina_input_dir)
        op_path: Path = (gnina_output_dir / lower_path).resolve()
        # determine what is in output
        if op_path.is_file():
            offset = 0
            with open(inp_path) as f:
                mol_names_inp: list[str] = [
                    item.strip().split("\n")[0].split(" ")[0]
                    for item in f.read().strip().split("$$$$")[:-1]
                ]
                mol_names_inp_set: set[str] = set(mol_names_inp)
            with open(op_path) as f:
                mol_names_op: list[str] = [
                    item.strip().split("\n")[0].split(" ")[0]
                    for item in f.read().strip().split("$$$$")[:-1]
                ]
                mol_names_op_set: set[str] = set(mol_names_op)

            for mol in mol_names_inp:
                if not mol in mol_names_op_set:
                    logging.warning(f"{str(lower_path)} is missing {mol}")
                    mol_names_op_set.add(mol)

        else:
            logging.warning(f"{str(lower_path)} was not created")

