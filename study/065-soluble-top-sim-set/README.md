
# 065-soluble-top-sim-set
Goal: determine statistics of the top compounds of the similar to top diversity set. Useful for determine if to keep / throw out a molecule during visual inspection
- Inputs: concat SDF of the top compounds
- Outputs: csv with each compounds statistics. Csv index aligns with align in SDF

## How To Use:
1) Run the script
- Check paths go to correct location
- Run it: pixi run -e logs-pred python molecule_statistics.py

## Data
top_dock_statistics: data about each molecule. Molecule index = index in SDF of input. Holds: Name,LogS,CNN_VS,CNNaffinity,Group,Molar Mass,Heavy Atoms,PAINS Flags,SMILES,Soluability,Notes

## Analysis
molecule_statistics.py: Takes in an SDF file, calculates a number of statistics, and places into a csv file
predefined_models.py: library to help with finding LogS
models/ holds pretrained models for predicted LogS
