# 031-validate-pharm0top-div
Goal: determine which pharmacophores are actually interacting in each docked molecule
- Inputs: csvs that list all interactions for each molecule in each region, top diversity set, each molecules list of pharmacophores
- Outputs: each molecule with a separate input json where non-important pharms are disabled

## Data
pharm_enable_lists: if each region's molecule's pharmacohpores are enabled or disabled.
- Rows: each pharmacophore (1st = index 0)
- Cols: each molecule (1st = 1st molecule in concat list = highest CNN)
script_output: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on script output
visual_inspect: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on visual inspection of low pharm molecules from script

## Analysis
find_imp_pharms: Will take in pharmacophores for each sdf and its list of interactions to determine key pharmacophores