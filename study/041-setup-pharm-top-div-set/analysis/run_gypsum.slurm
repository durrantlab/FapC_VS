#!/bin/bash
#SBATCH --job-name=gypsum                	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=16             	 				 # Number of CPU cores per task
#SBATCH --mem=32G                     	 				 # Memory allocation
#SBATCH --time=12:00:00                    				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/%A_%a.out                          # Output log path
#SBATCH --error=logs/%x_%A_%a.err                        # Error log path

module purge
module load pixi


echo "Getting arguments from the job array..."
ARGS=$(awk -v line=$((SLURM_ARRAY_TASK_ID + 1)) 'NR == line {print $0}' "job_list.txt")
LOG="${OUT%.sdf}.log"
echo "Done!"


echo "Running pharmit..."
bash -c "pixi run gypsum-dl $ARGS --min_pH 6 --max_pH 7.4" | tee "$LOG"
echo "Done!"