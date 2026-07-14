import sys
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem

RDLogger.DisableLog("rdApp.warning")


def main(curr_db_dir: Path, fixed_db_dir: Path):
    # go through each molecule in curr DB
    db_sdf_list: list[Path] = [
        item
        for item in curr_db_dir.iterdir()
        if item.is_file() and item.suffix == ".sdf"
    ]
    params = AllChem.ETKDGv3()
    params.numThreads = 0
    for db_sdf in db_sdf_list:
        # read in and add 3D coords
        mols: list = Chem.SDMolSupplier(str(db_sdf), removeHs=False)
        fixed_mols: list = []
        for mol in mols:
            mol = Chem.AddHs(mol)
            cids = AllChem.EmbedMultipleConfs(mol, numConfs=2, params=params)
            results = AllChem.UFFOptimizeMoleculeConfs(mol, numThreads=0, maxIters=350)
            # print(results)
            fixed_mols.append(mol)
        # write out
        writer = Chem.SDWriter(fixed_db_dir / db_sdf.name)
        for mol in fixed_mols:
            for conf in mol.GetConformers():
                writer.write(mol, confId=conf.GetId())
        writer.close()


if __name__ == "__main__":
    curr_db_dir: Path = (DIR_SCRIPT / "db_mols").resolve()
    fixed_db_dir: Path = (DIR_SCRIPT / "db_mols_fixed").resolve()
    main(curr_db_dir, fixed_db_dir)
