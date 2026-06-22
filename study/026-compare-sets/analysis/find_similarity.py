from pathlib import Path
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit import RDLogger


DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


def main(top_div_set_dir: Path, exp_set_file: Path, op_dir: Path):
    """Will determine the tanimoto / other similaries between each
    top div set and each exp set. Will create a .txt writeup file
    describing it

    Args:
        top_div_set_dir (Path): where top div set sdfs are stored
        exp_set_file (Path): where exp set sdf is stored
        op_dir (Path): where outputs are stored
    """
    # read in experimental set
    RDLogger.DisableLog('rdApp.warning')
    suppl = Chem.SDMolSupplier(str(exp_set_file))
    experimental_mols = [x for x in suppl]

    # read in the top div sets into one
    suppl = Chem.SDMolSupplier(str(exp_set_file))
    div_sdf_list: list[Path] = [item for item in top_div_set_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
    div_mols: list = []
    for div_sdf in div_sdf_list:
        suppl = Chem.SDMolSupplier(str(div_sdf))
        div_mols.extend([x for x in suppl])

    # for each experimental molecule
    op: str = ""
    fpgen = AllChem.GetRDKitFPGenerator()
    for exp_ind, exp_mol in enumerate(experimental_mols):
        exp_fp = fpgen.GetFingerprint(exp_mol)
        div_fps = [DataStructs.TanimotoSimilarity(fpgen.GetFingerprint(x), exp_fp) for x in div_mols]
        div_fps_inds = zip(div_fps, list(range(0,len(div_fps))))        
        most_sim: list[int | float] = max(div_fps_inds, key=lambda x: x[0])
        # create images
        photo_path: Path = Path(op_dir / "photos" / f"{exp_ind}_div_similar.png").resolve()
        draw_image(div_mols[most_sim[1]], photo_path)
        photo_path: Path = Path(op_dir / "photos" / f"{exp_ind}_exp.png").resolve()
        draw_image(exp_mol, photo_path)
        # output data
        op = op + f"Experimental Molecule: {exp_ind}\n"
        op = op + f"Most similar to div set molecule: {most_sim[1]}\n"
        op = op + f"Tanimoto Similarity: {most_sim[0]}\n\n"

    log_file: Path = Path(op_dir / "log.txt").resolve()
    with open(log_file, "w") as f:
        f.write(op)


def draw_image(mol, photo_path: Path):
    AllChem.Compute2DCoords(mol)
    img = Draw.MolToImage(mol, size=(400, 400))
    if not photo_path.parent.is_dir():
        photo_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(photo_path)   # it's a standard PIL image







if __name__ == "__main__":
    # inputs
    top_div_set_dir: Path = Path(DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs")
    exp_set_file: Path = Path(DIR_STUDY / "026-compare-sets" / "data" / "exp_set.sdf")
    op_dir: Path = Path(DIR_STUDY / "026-compare-sets" / "data")

    main(top_div_set_dir, exp_set_file, op_dir)


