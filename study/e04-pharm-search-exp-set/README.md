
# e04-pharm-search-exp-set
Goal: find the 5000 most similar molecules to each molecule of experimental set
-   Inputs: a folder where each molecule has a separate input json where non-important pharms are disabled
-   Outputs: many similar molecules for each molecule in top div set. Each molecule will have an SDF with it’s similar molecules, and csv file of the best molecules. Both ranked with rmsd. /mol#.csv and /mol#.sdf/

## How To Use:
1)  Prep for pharmacophore search
-   Create pharmit input scripts running create_batch_job
-   Check the paths are correct
-   Run with pixi
1)  Run pharmit search
-   chmod +x run_pharmit_search.sh
-   ./run_pharmit_search.sh

## Data
search_output/ holds the output of pharmacophore search
-   mol#.sdf: the 2000 similar molecules to that molecule of that region. In order of RMSD.
-   RMSD = how different base molecules pharmacophores are to this molecules pharmacophores
-   mol#.csv: CSV holding index,name,rmsd,search_iteration for each molecule, sorted by RMSD

## Analysis
[create_batch_job.py](/study/e04-pharm-search-exp-set/analysis/create_batch_job.py): Will take in pharmits input files and create a slurm to run the iterative pharm script.
[pharm_search.slurm](/study/e04-pharm-search-exp-set/analysis/pharm_search.slurm): slurm script for the pharmit search batch job
[iterative_pharm.py](/study/e04-pharm-search-exp-set/analysis/iterative_pharm.py): the iterative pharm program command line wrapper
run_pharmit_search.sh: bash script that runs the batch jobs (created)
temp/ folder that holds temp data for iterative_pharm. Files deleted when iterative pharmit completes (created)
