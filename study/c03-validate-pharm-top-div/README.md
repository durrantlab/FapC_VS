
# c03-validate-pharm-top-div
Goal: determine which pharmacophores are actually interacting in each docked molecule
-   Inputs: csvs that list all interactions for each molecule in each region, top diversity set (concat SDF, 1 for each region), each molecules list of pharmacophores (concat JSON, 1 for each region)
-   Outputs: each molecule with a separate input json where non-important pharms are disabled

## How To Use:
1)  Using pharm list, determine which are actually important based on all interactions csv
-   Done in find_imp_pharms
-   Make sure all the paths point to the correct spot
-   Run with pixi
1)  Visually inspect molecules with low pharmacophore counts
-   Download: pharmit pharmacophore jsons, best_drugs from 025, protonated protein
    -   Download from script_output
-   Look in the log file for all molecules with low pharm counts (marked with warning)
-   Open it in pharmit server and PyMol.
-   Pymol have protein be all sticks, centered on drug
-   For pharmit, enable only pharms enabled in the json
-   Look for missed interactions, and pharms that could be enabled.
-   If one can be enabled, mark it here and manually enable it in the file
-   *Region2, mol5: enabled last hydrogen acceptor (implemented)*
-   *Region 2, mol6: thrown out (implemented)*
-   *Region 2, mol8: enabled last hydrophobic, 3rd hydrophobic (implemented)*
-   *Region 3, mol1: enabled last hydrophobic (implemented)*
-   *Region 3, mol4: throw out (implemented)*
-   *Region 3, mol6: throw out (implemented)*
-   Then reupload the edited pharmacophore jsons into visual_inspect folder (need to create)

## Data
pharm_enable_lists: if each region's molecule's pharmacohpores are enabled or disabled.
-   Rows: each pharmacophore (1st = index 0)
-   Cols: each molecule (1st = 1st molecule in concat list = highest CNN)
script_output: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on script output
visual_inspect: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on visual inspection of low pharm molecules from script

## Analysis
[find_imp_pharms](/study/c03-validate-pharm-top-div/analysis/find_imp_pharms.py): Will take in pharmacophores for each sdf and its list of interactions to determine key pharmacophores

## Logs
find_imp_pharms.log: holds output of pharmacophore enabling / disabling script. Check to see if any have 3 or less enabled
