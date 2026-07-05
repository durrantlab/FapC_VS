from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()



def main(gnina_input_dir: Path, gnina_output_dir: Path):
    # extract all inputs 
    for inp_path in Path(gnina_input_dir).rglob("group*.sdf"):
        lower_path: Path = inp_path.relative_to(gnina_input_dir)
        op_path: Path = (gnina_output_dir / lower_path).resolve()
        # determine what is in output
        if op_path.is_file():
            offset = 0
            with open(inp_path) as f:
                mol_names_inp: set[str] = set([item.strip().split("\n")[0].split(" ")[0] for item in f.read().strip().split("$$$$")[:-1]])
            with open(op_path) as f:
                mol_names_op: set[str] = set([item.strip().split("\n")[0].split(" ")[0] for item in f.read().strip().split("$$$$")[:-1]])
            for mol_ind in range(len(mol_names_inp)):
                if(mol_names_inp != mol_names_op):
                    offset = offset + 1
            if(offset > 0):
                print(f"{str(lower_path)} is missing molecules")
                print(mol_names_inp)
                print(mol_names_op)
        else:
            print(f"{str(lower_path)} was not created")





if __name__ == "__main__":
    gnina_input_dir: Path = (DIR_SCRIPT / ".." / "data" / "cleaned_compounds").resolve()
    gnina_output_dir: Path = (DIR_SCRIPT / ".." / "data" / "docked_compounds").resolve()
    main(gnina_input_dir, gnina_output_dir)


