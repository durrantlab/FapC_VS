#!/bin/bash
#SBATCH --job-name=pharm_search                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=128G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=test.out                               # Output log path

module purge
module load pixi

pixi run -e pharmit pharmit dbsearch -max-hits 2000 -max-weight 750 -sort-rmsd -dbdir ../data/DB -extra-info -in D:\FapC_VS\study\031-validate-pharm-top-div\data\region_1\mol8_input.json -out D:\FapC_VS\study\032-pharm-search-top-div\data\search_output\region_1\mol8_input.sdf D:\FapC_VS\study\032-pharm-search-top-div\data\search_output\region_1\mol8_input.txt