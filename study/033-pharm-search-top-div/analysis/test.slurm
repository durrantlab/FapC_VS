#!/bin/bash
#SBATCH --job-name=pharm_search                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=8             	 				 # Number of CPU cores per task
#SBATCH --mem=16G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=test.out                               # Output log path

module purge
module load pixi

pixi run -e pharmit pharmit dbsearch -max-weight 750 -sort-rmsd -extra-info -in /ihome/jdurrant/irh24/Projects/FapC_VS/study/031-validate-pharm-top-div/data/region_3/mol9_input.json -out /ihome/jdurrant/irh24/Projects/FapC_VS/study/033-pharm-search-top-div/data/search_output/region_3/mol9_input.sdf -out /ihome/jdurrant/irh24/Projects/FapC_VS/study/033-pharm-search-top-div/data/search_output/region_3/mol9_input.txt -max-hits 2000 -dbdir /ihome/jdurrant/irh24/Projects/FapC_VS/study/032-create-pharm-db/data/DB
