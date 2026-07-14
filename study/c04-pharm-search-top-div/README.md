
# 033-pharm-search-top-div
Goal: find the 2000 most similar molecules to each top molecule of diversity set. Will keep running search removing pharmacophores until all 2000 found.
- Inputs: each molecule with a separate input json where non-important pharms are disabled
- Outputs: many similar molecules for each molecule in top div set. Each molecule will concat SDFs of similar molecules, and csv file of the best molecules ranked via rmsd. Organized region_#/mol#.sdf(csv)

## How To Use:
1) Prep for pharmacophore search
- Create pharmit input scripts running create_batch_job
- Check the paths are correct
- Run with pixi
2) Run pharmit search
- chmod +x run_pharmit_search.sh
- ./run_pharmit_search.sh

## Data
search_output/ holds the output of pharmacophore search
- region_#/ similar molecules of each region
- mol#.sdf: the 2000 similar molecules to that molecule of that region. In order of RMSD.
 - RMSD = how different base molecules pharmacophores are to this molecules pharmacophores
- mol#.csv: CSV holding index,name,rmsd,search_iteration for each molecule, sorted by RMSD

## Analysis
create_batch_job.py: Will take in pharmits input files and create a slurm to run the iterative pharm script.
iterative_pharm.py: Using 1 pharmacophore list input will iteratively run pharmacophore searches with pharmit, removing pharmacophores in BFS style, until only 3 remain or max_mol compounds are found.
pharmit_search.py: library to help with querying pharmit server API
pharm_search.slurm: slurm script for the pharmit search batch job
run_pharmit_search.sh: bash script that runs the batch jobs (created)
temp/ folder that holds temp data for iterative_pharm. Files deleted when iterative pharmit completes (created)
