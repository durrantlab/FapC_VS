
# c01-key-top-div-inter
Goal: for each ligand, determine the interactions present between it and the protein
- Inputs: top molecules from div set docking (concat SDFs, format of region_#_concat.sdf in dir together), protonated PDB
- Outputs: each region has a csv report that holds each molecules residue interaction / types. It stores false if no interaction present in that molecule, or . separated list of atom indices in ligand
 - Molecule index is same as index of molecule in sdf, which starts at 1

## How To Use:
1) Find every molecules interaction with the protein it is in
- Check that it points to location of top docked ligands in concatenated files, to protonated protein pdb, and the data file of this section
- Run it with pixi
2) NOTE: the csv will hold the atoms each residue interacts with, starting its indexing at 1. The SDFs / pymol start atom indexing at 1. RdKit starts at 0.
The interaction naming is based on what the ligand is doing
- Ex: if ligand is HBond acceptor, that is the name given

## Data
`region_<>_interacts`: for each region holds every top molecule's interactions
- Each column is a different protein residue / interaction it can be involved in
- Each row is a different molecule
- Each sublist (seperated by .) is list of atoms involved in that interaction type with that residue. If it is false, means that the molecule does not interact with it. Atom indexing starts at 1, the type depends on the side of the interaction the ligand is involved in.

## Analysis
find_interacts.py: Will take in number of SDF files and a protein file and determine the interactions present for each ligand and which atoms are involved. Output into a csv
