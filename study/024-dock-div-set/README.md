
# 024-dock-div-set
Goal: dock the diversity set with GNINA
- Input: each molecule with a separate SDF, setup with hydrogens and different conforms
- Output: many SDFs with the same molecules in them, but now they are moved to be in docked location and hold data about the scoring inside the SDF

## How To Use:
1) Put together (concatenate) SDF files
- Ensure script (concat_sdf_files) points to where mass, separate SDFs are located and where the concatenated ones should be placed
 - *Decided on 30 SDFs*
- Run the script
2) Create all Gnina inputs
- Ensure all the paths point to the correct spot 
- Run create_gnina_job_list: pixi run python create_gnina_job_list.py
3) Run Gnina
- chmod +x run_gnina.sh
- ./run_gnina.sh

## Data
concat_lig: holds the prepped ligands, when put together into large SDFs
docked_compounds: each region has a subfolder. Inside, for each concat_lig file, will hold every ligand conform's docked pose and CNN score.

## Analysis
concat_sdf_files: takes in a list of SDFs, each with different conformers of the same molecule, and puts them into N different concatted SDFs together. Allows for 1 docking job to do much more.
create_gnina_job_list: takes in all boxes, ligands and the protein and creates gnina inputs to dock every ligand to every box.
- job_list.txt: holds the arguments for each job. Each line is a different job.
- run_gnina.sh: bash script that submits the jobs
dock.slurm: batch job specification for the gnina jobs
