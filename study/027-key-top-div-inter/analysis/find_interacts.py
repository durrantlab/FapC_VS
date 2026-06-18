from typing import Any
from pandas.core.frame import DataFrame
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
    rdkit_prot = Chem.MolFromPDBFile(str(protein_file), removeHs=False)
    protein_mol = plf.Molecule(rdkit_prot)

    div_sdf_list: list[Path] = [item for item in docked_ligands_dir.iterdir() if item.is_file() and item.suffix == ".sdf"]
    op = ""
    for div_sdf in div_sdf_list:
        print(div_sdf)
        
        pose_iterable = plf.sdf_supplier(str(div_sdf))
        fp = plf.Fingerprint(vicinity_cutoff=10, \
                            interactions=["Hydrophobic", "HBDonor", "HBAcceptor", "PiStacking",
                                          "Anionic", "Cationic", "CationPi", "PiCation"],
                             parameters={"Hydrophobic":{"distance":5}, \
                                        "HBDonor":{"distance":4.0}, \
                                        "HBAcceptor":{"distance":4.0}, \
                                        "Anionic":{"distance":8}, \
                                        "Cationic":{"distance":8}, \
                                        "PiStacking":{"ftf_kwargs": {"distance": 8},
                                                      "etf_kwargs": {"distance": 8}}})
        fp.run_from_iterable(pose_iterable, protein_mol)
        
        lig_inter_list: list[dict[str,dict[str,list[int]]]] = []
        """D1: each molecule D2: each protein res D3: each interaciton D4: list of atoms interacting"""
        for mol_indx in range(len(pose_iterable)): # go through every molecule
            lig_inter_list.append({})
            for (lig_res, prot_res), interactions in fp.ifp[mol_indx].items(): # go through every interaction for this one
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
        
        df: df = fp.to_dataframe(index_col="Pose")
        df_list: list[list] = [df.columns.tolist()] + df.to_numpy().tolist()

        for mol_indx in range(len(df_list[1:])):
            act_indx = mol_indx + 1
            temp_lig_inters: dict[str,dict[str,list[int]]] = lig_inter_list[mol_indx]
            for inter_indx in range(len(df_list[0])):
                for (prot_name, atoms_) in temp_lig_inters.items():
                    for (inter_name, atoms) in atoms_.items():
                        if prot_name == df_list[0][inter_indx][1] and \
                                inter_name == df_list[0][inter_indx][2]:
                            df_list[act_indx][inter_indx] = ".".join([str(item) for item in atoms])

        csv_op: Path = (op_dir / f"{'_'.join(div_sdf.name.split('_')[0:2])}_interacts.csv").resolve()
        with open(csv_op, "w") as f:
            # add in headers
            headers: list[list[Any]] = [list(row) for row in zip(*df_list[0])]
            for header in headers:
                f.write(",".join(header) + "\n")
            # add in data
            for line in df_list[1:]:
                f.write(",".join([str(item) for item in line]) + "\n")




if __name__ == "__main__":
    # inputs
    docked_ligands_dir: Path = (DIR_STUDY / "025-filter-gnina-op" / "data" / "best_drugs").resolve()
    protein_file: Path = (DIR_STUDY / "023-prep-protein-dock" / "data" / "9nqd_protonated.pdb").resolve()
    op_dir: Path = (DIR_STUDY / "027-key-top-div-inter" / "data").resolve()
    main(docked_ligands_dir, protein_file, op_dir)

