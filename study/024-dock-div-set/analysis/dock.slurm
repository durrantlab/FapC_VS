#!/bin/bash
#SBATCH --job-name=psma1_controls_dock       	 		 # Job name
#SBATCH --cluster=gpu				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --gres=gpu:1                  			     	 # Number of GPUs
#SBATCH --constraint=a100               			     # Use a100 GPUS
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=32             	 				 # Number of CPU cores per task
#SBATCH --mem=128G                     	 				 # Memory allocation
#SBATCH --time=6-00:00:00               				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/%A_%a.out                          # Output log path
#SBATCH --error=logs/%x_%A_%a.err                        # Error log path
#SBATCH --mail-user=nag81@pitt.edu	   					 # Sends email on job
#SBATCH --mail-type=ALL                  				 # Notifications for job start, end, fail, etc.


module purge
module load cuda/11.7.0
module load python/3.7.0
module load gnina

echo "Getting arguments from the job array..."
ARGS=$(awk -v line=$((SLURM_ARRAY_TASK_ID + 1)) 'NR == line {print $0}' "$JOB_LIST")
echo "Done!"

echo "Getting current receptor and config..."
RECEPTOR=$(echo "$ARGS" | grep -oP '(?<=--receptor )\S+')
CONFIG=$(echo "$ARGS" | grep -oP '(?<=--config )\S+')
OUT=$(echo "$ARGS" | grep -oP '(?<=--out )\S+')
echo "Done!"

LOG="${OUT%.sdf}.log"

echo "Receptor: $RECEPTOR"
echo "Config:   $CONFIG"
echo "Ligand:   $LIGAND_FILE"
echo "Output:   $OUT"

echo "Running gnina..."
bash -c "gnina --cpu $SLURM_CPUS_PER_TASK $ARGS" | tee "$LOG"
echo "Done!"
