
# b01-prep-protein-dock
Goal: Setup the protein for docking with [reduce](https://github.com/rlabduke/reduce)
- Input: each molecule with a separate SDF, setup with hydrogens and different conforms
- Output: organized by region_#/ligs_###.sdf, where each SDF has many molecules / conforms inside and are docked / scored. Each molecule is present in each region folder. Number of SDFs in each region specified.

## How To Use:
1) Setup protonate.sh
- Make sure that PDB_inp points to the cleared FTMap
- Make sure the PDB_op points to this files data folder
2) Run protonate.sh: 
- Allow script to be run: chmod +x prep_protein.sh
- Run script: ./prep_protein.sh

## Data
9nqd_protonated.pdb: the protonated pdb, created with reduce

## Analysis
[prep_protein.sh](/study/b01-prep-protein-dock/analysis/prep_protein.sh): will create protonated protein using reduce
