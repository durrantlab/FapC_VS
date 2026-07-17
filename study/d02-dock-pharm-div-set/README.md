
# d02-dock-pharm-div-set
Goal: dock the similar to top diversity set
- Input: SDFs with many molecules (which have many conformers), setup with hydrogens and different conforms. Organized: region_# / mol# / group_# / [].sdf
- Output: many SDFs with the many different molecules in them, but now they are moved to be in docked location and hold data about the scoring inside the SDF. Organized: region_#/mol#/group_#.sdf

## How To Use:
1) Create all Gnina inputs
- NOTE: will only do clean copy if copy doesnt already exist, only runs gnina if output sdf doesnt already exist. Therefore if they do, and you want to rerun, delete those files
- Will copy over the SDFs to cleaned_compounds, same except it removes the settings molecule at top of gypsum
 - Will store those settings in a settings.sdf at top of that directory
- Ensure all the paths point to the correct spot 
- Run create_gnina_job_list: pixi run python create_gnina_job_list.py
2) Sanity check: gypsum cleaning
- Make sure that the head looks correct, transitions correct, end is correct
- Make sure the name of 1st and last compounds are same as in original
3) Run Gnina
- chmod +x run_gnina.sh
- ./run_gnina.sh
4) Sanity check: all
- Check that the group_x files have same molecules as group_x file in 041
- Check they are docked into correct box
- See if docking looks good or not

## Data
cleaned_concats: takes the prepped ligands from gypsum and removes the first settings. Organized: region_#/mol#/group_#.sdf
- Has a gypsum_settings.sdf at root that holds what the old headers used to be
docked_compounds: each ligand moved to pocket it was docked to (docked to same pocket as parent molecule). Organized same as cleaned_concat

## Analysis
create_gnina_inputs.py: Takes in all the SDF to be docked, remove gypsum settings molecule, then creates gnina inputs to be run
run_gnina.sh: submits the batch jobs (created)
dock.slurm: settings for the batch job
job_list.txt: list of arguments for each run of gnina (created)
check_output.py: will check that each molecule of input was successfully docked
