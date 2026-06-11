import warnings

with warnings.catch_warnings(record=True):
    from pathlib import Path
    import prolif as plf
    from rdkit import Chem

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT  / ".." / "..").resolve()


def main(docked_ligands_dir: Path, protein_file: Path, op_dir: Path):
    """Will take in number of SDF files and a protein file and determine
    the interactions present for each ligand

    Args:
        docked_ligands_dir (Path): where the ligands stored.
        protein_file (Path): the protein pdb they were docked too
        op_dir (Path): where output data will be placed
    """
    # read in protein
    rdkit_prot = Chem.MolFromPDBFile(protein_file, removeHs=False)
    protein_mol = plf.Molecule(rdkit_prot)

    div_sdf_list: list[Path] = [item for item in docked_ligands_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
    op = ""
    for div_sdf in div_sdf_list:
        print(div_sdf)
        pose_iterable = plf.sdf_supplier(div_sdf)
        fp = plf.Fingerprint()
        fp.run_from_iterable(pose_iterable, protein_mol)
        df = fp.to_dataframe(index_col="Pose")
        csv_op: Path = (op_dir / f"{"_".join(div_sdf.name.split("_")[0:2])}_interacts.csv").resolve()
        df.to_csv(str(csv_op), index=False)






if __name__ == "__main__":
    # inputs
    docked_ligands_dir: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs").resolve()
    protein_file: Path = (DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb").resolve()
    op_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data").resolve()
    main(docked_ligands_dir, protein_file, op_dir)

