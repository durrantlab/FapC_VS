import os
import shutil
import tempfile
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


def main(
    sdf_db_path: Path,
    db_main_path: Path,
    skip_file_format: bool = False,
    DIR_SCRIPT: Path = DIR_SCRIPT,
):
    """Takes in library of sdf molecules, edits files to be
    correct format and creates a script that (when run)
    will setup the database

    Args:
        sdf_db_path: where the sdf library is
        db_main_path: where the db will be placed
    """

    # get all sdf files
    sdf_file_list: list[Path] = [
        item
        for item in sdf_db_path.iterdir()
        if item.is_file() and item.suffix == ".sdf"
    ]

    # edit all files to have different names for each molecule
    if not skip_file_format:
        index = 0
        for sdf_file in sdf_file_list:
            print(f"fixing {sdf_file}")
            index = fix_names(sdf_file, index)

    # create main db if it doesnt exist
    if not db_main_path.is_dir():
        db_main_path.mkdir(parents=True, exist_ok=True)

    # create the job list
    job_list_path: Path = (DIR_SCRIPT / "job_list.txt").resolve()
    job_num = 0
    with open(job_list_path, "w") as f:
        for sdf_file in sdf_file_list:
            # determine if its respective DB exists
            db_path: Path = (db_main_path / f"{sdf_file.name.split('.')[0]}").resolve()
            if db_path.is_dir():
                # determien if valid
                if (db_path / "dbinfo.json").resolve().exists():
                    print(f"{db_path.name} is already valid")
                    continue
                else:
                    print(f"{db_path.name} is invalid. Deleting")
                    shutil.rmtree(db_path)
            else:
                print(f"{db_path.name} does not exist yet")
            # if doesnt exist / was invalid (and deleted)
            f.write(f"-dbdir {db_path} -in {sdf_file}\n")
            job_num = job_num + 1

    # create bash to run db creator
    bash_path: Path = (DIR_SCRIPT / "create_db.sh").resolve()
    with open(bash_path, "w") as f:
        f.write(f"sbatch --array=0-{job_num-1} --export=ALL create_db.slurm")


def fix_names(sdf_file: Path, index: int) -> int:
    with (
        open(sdf_file) as src,
        tempfile.NamedTemporaryFile(
            "w", delete=False, dir=sdf_file.parent.resolve(), newline=""
        ) as tmp,
    ):
        tmpname = tmp.name
        lines = []
        no_name = True

        for line in src:
            if no_name:
                lines.append(line)
                if len(lines) > 2 and lines[-2].startswith(
                    ">  <PUBCHEM_EXT_DATASOURCE_REGID>"
                ):
                    lines[0] = lines[-1]
                    for line_ in lines:
                        tmp.write(line_)
                    no_name = False
            else:
                if line.startswith("$$$$"):
                    no_name = True
                    lines = []
                tmp.write(line)

    os.replace(tmpname, sdf_file)

    return index


if __name__ == "__main__":
    # inputs
    sdf_db_path: Path = Path("/ihome/jdurrant/irh24/Projects/molport_cmpds").resolve()
    # sdf_db_path: Path = Path("F:\\FapC_VS\\study\\032-create-pharm-db\\data\\").resolve() # for testing
    # db_main_path: Path = (DIR_SCRIPT / ".." / "data" / "DB").resolve()
    db_main_path: Path = Path("/ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB").resolve()

    main(sdf_db_path, db_main_path, True)
