# 024-dock-div-set
Goal: dock the diversity set

## Data
concat_lig: holds the prepped ligands, when put together into large SDFs
docked_compounds: each region has a subfolder. Inside, for each concat_lig file, will hold every ligand conform's docked pose and CNN score.

## Analysis
concat_sdf_files: takes in a list of SDFs, each with different conformers of the same molecule, and puts them into N different concatted SDFs together. Allows for 1 docking job to do much more.
create_gnina_job_list: takes in all boxes, ligands and the protein and creates gnina inputs to dock every ligand to every box.
- job_list.txt: holds the arguments for each job. Each line is a different job.
- run_gnina.sh: bash script that submits the jobs
dock.slurm: batch job specification for the gnina jobs