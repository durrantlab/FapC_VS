from pathlib import Path


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


def main(sdf_db_path: Path, db_op_path: Path):
    """Takes in library of sdf molecules, edits files to be
    correct format and creates a script that (when run)
    will setup the database

    Args:
        sdf_db_path (Path): where the sdf library is
        db_op_path (Path): where the db will be placed
    """
    
    # get all sdf files
    sdf_file_list: list[Path] = [item for item in sdf_db_path.iterdir() if item.is_file() and item.suffix == ".sdf"]

    # edit all files to have different names for each molecule
    for sdf_file in sdf_file_list:
        print(f"fixing {sdf_file}")
        fix_names(sdf_file)
    
    # create script to create db
    with open((DIR_SCRIPT / "create_db.sh"), "w") as f:
        f.write("pixi run -e pharmit pharmit dbcreate -dbdir ../data/DB")
        for sdf_file in sdf_file_list:
            f.write(f" -in {sdf_file}")




def fix_names(sdf_file: Path):
    # read in file
    with open(sdf_file, "r") as f:
        mole_list = [item.split("\n") for item in f.read().split("\n$$$$\n")]
    # for each molecule edit the name
    for molecule in mole_list:
        if len(molecule) > 10:
            name_ind = next((i for i, ln in enumerate(molecule) if "PUBCHEM_EXT_DATASOURCE_REGID" in ln), -1) + 1
            name = molecule[name_ind].strip()
            molecule[1] = f"  {name}"
    # write out molecules
    with open(sdf_file, "w") as f:
        f.write("\n&&&&\n".join(["\n".join(item) for item in mole_list]))




if __name__ == "__main__":
    # inputs
    sdf_db_path: Path = Path("/ihome/jdurrant/irh24/Projects/molport_cmpds").resolve()
    #sdf_test_path: Path = Path("F:\\FapC_VS\\study\\032-create-pharm-db\\data\\").resolve()
    db_op_path: Path = (DIR_STUDY / "data").resolve()

    main(sdf_db_path, db_op_path)


