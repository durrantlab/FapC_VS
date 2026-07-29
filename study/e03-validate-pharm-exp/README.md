
# e03-validate-pharm-exp
Goal: determine which pharmacophores are actually interacting in each docked molecule 
- Inputs: csvs that list all interactions for each molecule, experimental set (in concat SDF), each molecules list of pharmacophores (in concat JSON)
- Outputs: each molecule has a separate input json where non-important pharms are disabled. /mol#_input.json

## How To Use:
1) Using pharm list, determine which are actually important based on all interactions csv
- Done in find_imp_pharms
- Make sure all the paths point to the correct spot
- Run with pixi
2) Visually inspect molecules with low pharmacophore counts
- Download: pharmit pharmacophore jsons, experimental molecule SDF from 026, protonated protein
 - Download from script_output
- Look in the log file for all molecules with low pharm counts (marked with warning)
- Open it in pharmit server and PyMol. 
 - Pymol have protein be all sticks, centered on drug
 - For pharmit, enable only pharms enabled in the json
- Look for missed interactions, and pharms that could be enabled.
- If one can be enabled, mark it here and manually enable it in the file
 - *mol0: enable 3rd aromatic, 2nd to last hydrogen*
 - *mol2: added none, just run it*
- Then reupload the edited pharmacophore jsons into visual_inspect folder (need to create)

## Data
pharm_disable_lists: if each region's molecule's pharmacophores are enabled or disabled.
- Rows: each pharmacophore (1st = index 0)
- Cols: each molecule (1st = 1st molecule in concat list = highest CNN)
script_output: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on script output
visual_inspect: for each region, each molecule's pharmacophore json with pharmacophores enabled / disabled depending on visual inspection of low pharm molecules from script

## Analysis
[find_imp_pharms.py](/study/e03-validate-pharm-exp/analysis/find_imp_pharms.py): Will take in pharmacophores for each sdf and its list of interactions to determine key pharmacophores

## Logs
find_imp_pharms.log: holds output of pharmacophore enabling / disabling script. Check to see if any have 3 or less enabled

## Visualization
[check_pharms.pse](/study/e03-validate-pharm-exp/visualization/check_pharms.pse): pymol session used to visually check if certain pharmacophores could be enabled
