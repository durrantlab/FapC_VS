#!/bin/bash
#SBATCH --job-name=create_db                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=32G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/batch.out                          # Output log path

module purge
module load pixi


