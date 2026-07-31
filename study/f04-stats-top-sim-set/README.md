
# f04-stats-top-sim-set
Goal: determine statistics of the top compounds of the similar to experimental set. Then do visual inspection of top dockers.
-   Inputs: concat SDF of the top compounds
-   Outputs: csv with each compounds statistics. Csv index aligns with align in SDF

## How To Use:
1)  Run the script
-   Check paths go to correct location
-   Run it: pixi run -e logs-pred python molecule_statistics.py
1)  Visually check the top molecules
-   Setup a molport session
-   Upload all top hits (single SDFs) from 069-filter-gnina
-   Upload protonated protein from (023-prep-protein)
-   Have the CSV open (from this section). Uploaded to drive so it can be shared
-   Go through each molecule and see: is it strained, is it “boxed”, how is H-bond network, is it soluble, does it have PAINS, …

## Data
top_dock_statistics: data about each molecule. Molecule index = index in SDF of input. Holds: Name,LogS,CNN_VS,CNNaffinity,Group,Molar Mass,Heavy Atoms,PAINS Flags,SMILES,Soluability,Notes

## Analysis
[molecule_statistics.py](/study/f04-stats-top-sim-set/analysis/molecule_statistics.py): Takes in an SDF file, calculates a number of statistics, and places into a csv file
