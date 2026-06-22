# 027-key-top-div-inter
Goal: for each ligand, determine the interactions present between it and the protein and which atoms of the ligand are involved
- Inputs: top SDF outputs from div set scoring, protonated PDB
- Outputs: each region has a csv report that holds each molecules residue interaction / types. It stores false if no interaction present in that molecule, or . separated list of atom indices in ligand

## Data
region_[]_interacts: for each region holds every top molecule's interactions
- Each column is a different protein residue / interaction it can be involved in
- Each row is a different molecule
- Each sublist (seperated by .) is list of atoms involved in that interaction type with that residue. If it is false, means that the molecule does not interact with it.

## Analysis
find_interacts.py: Will take in number of SDF files and a protein file and determine the interactions present for each ligand and which atoms are involved. Output into a csv