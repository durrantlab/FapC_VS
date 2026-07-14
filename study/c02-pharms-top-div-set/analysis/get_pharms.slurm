#!/bin/bash
#SBATCH --job-name=get_pharms                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=128G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/batch.out                          # Output log path

module purge
module load pixi



pixi run -e pharmit pharmit pharma -in D:\FapC_VS\study\025-filter-gnina-op\data\best_drugs\region_1_concat.sdf -out D:\FapC_VS\study\028-pharms-top-div-set\data\region_1_concat.out
pixi run -e pharmit pharmit pharma -in D:\FapC_VS\study\025-filter-gnina-op\data\best_drugs\region_2_concat.sdf -out D:\FapC_VS\study\028-pharms-top-div-set\data\region_2_concat.out
pixi run -e pharmit pharmit pharma -in D:\FapC_VS\study\025-filter-gnina-op\data\best_drugs\region_3_concat.sdf -out D:\FapC_VS\study\028-pharms-top-div-set\data\region_3_concat.out