
import warnings
from pandas.core.frame import DataFrame
import pandas

with warnings.catch_warnings(record=True):
    from pathlib import Path

    import prolif as plf
    from rdkit import Chem

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def main(docked_ligands_dir: Path, protein_file: Path, 
    op_dir: Path) -> None:
    """Will take in number of SDF files and a protein file and determine
    the interactions present for each ligand

    Args:
        docked_ligands_dir: where the ligands stored.
        protein_file: the protein pdb they were docked too
        op_dir: where output data will be placed
    """
    # read in protein
    rdkit_prot = Chem.MolFromPDBFile(str(protein_file), removeHs=False)
    protein_mol = plf.Molecule(rdkit_prot)

    div_sdf_list: list[Path] = [
        item
        for item in docked_ligands_dir.iterdir()
        if item.is_file() and item.suffix == ".sdf"
    ]
    op = ""
    for div_sdf in div_sdf_list:
        print(div_sdf)

        pose_iterable = plf.sdf_supplier(str(div_sdf))
        fp = plf.Fingerprint(
            vicinity_cutoff=10,
            interactions=[
                "Hydrophobic",
                "HBDonor",
                "HBAcceptor",
                "PiStacking",
                "Anionic",
                "Cationic",
                "CationPi",
                "PiCation",
            ],
            parameters={
                "Hydrophobic": {"distance": 5},
                "HBDonor": {"distance": 4.0},
                "HBAcceptor": {"distance": 4.0},
                "Anionic": {"distance": 8},
                "Cationic": {"distance": 8},
                "PiStacking": {
                    "ftf_kwargs": {"distance": 8},
                    "etf_kwargs": {"distance": 8},
                },
            },
        )
        fp.run_from_iterable(pose_iterable, protein_mol)

        lig_inter_list: list[dict[str, dict[str, list[int]]]] = []
        """D1: each molecule D2: each protein res D3: each interaciton D4: list of atoms interacting"""
        for mol_indx in range(len(pose_iterable)):  # go through every molecule
            lig_inter_list.append({})
            for (lig_res, prot_res), interactions in fp.ifp[
                mol_indx
            ].items():  # go through every interaction for this one
                prot_name: str = f"{prot_res.name}{prot_res.number}.{prot_res.chain}"
                lig_inter_list[-1][prot_name] = {}
                for int_name, metadata_list in interactions.items():
                    lig_inter_list[-1][prot_name][int_name] = []
                    for md in metadata_list:
                        lig_atoms: tuple[int] = md["parent_indices"]["ligand"]
                        for lig_atom_ in lig_atoms:
                            lig_atom = lig_atom_ + 1
                            if not lig_atom in lig_inter_list[-1][prot_name]:
                                lig_inter_list[-1][prot_name][int_name].append(lig_atom)

        df = create_interact_df(fp, lig_inter_list)

        csv_op: Path = (
            op_dir / f"{'_'.join(div_sdf.stem.split('_')[0:2])}_interacts.csv"
        ).resolve()
        df.to_csv(csv_op, index=False)


def create_interact_df(fp: plf.Fingerprint, 
                        lig_inter_list: list[dict[str, dict[str, list[int]]]]
                        ) -> DataFrame:
    """Takes in the interaction fingerprint and creates a DF
    where each col is a different interaction / interaction type and row is
    a different molecule. 

    If interaction exists, lists atom indicies involved in molecule. If it 
    does not, says false.

    Headers are (1) ligand residue involved (2) prot residue involve (3) iteraction
    type

    Args:
        fp (plf.Fingerprint): prolif fingerprint of an docked concat SDF

    Returns:
        DataFrame: pandas dataframe with setup described above
    """
    df: DataFrame = fp.to_dataframe(index_col="Pose").astype(str)

    for mol_indx, prot_ress in enumerate(lig_inter_list):  # go through every molecule
        for prot_res, interactions in prot_ress.items():
            for interaction, atoms in interactions.items():
                df.loc[mol_indx, pandas.IndexSlice[:, prot_res, interaction]] = ".".join(
                            [str(item) for item in atoms]
                        )
    df = df.droplevel(3, axis=1)
    return df
