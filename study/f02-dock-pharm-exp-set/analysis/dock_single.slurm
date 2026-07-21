#!/bin/bash
#SBATCH --job-name=fc_dock_pdiv             	 		 # Job name
#SBATCH --cluster=smp				   	 				 # Use cluster with GPU support
#SBATCH --partition=preempt             				 # Use preempt partion (free)
#SBATCH --nodes=1                      					 # Number of nodes
#SBATCH --ntasks=1                     	 				 # Number of tasks
#SBATCH --cpus-per-task=4             	 				 # Number of CPU cores per task
#SBATCH --mem=8G                     	 				 # Memory allocation
#SBATCH --time=02:00:00               				 # Time limit (D-HH:MM:SS)
#SBATCH --output=logs/%A.out                             # Output log path
#SBATCH --error=logs/%x_%A.err                          # Error log path


module purge
module load cuda/11.7.1
module load gnina

LOG="${OUT%.sdf}.log"

echo "Running gnina..."
gnina --cpu $SLURM_CPUS_PER_TASK \
    --receptor /ihome/jdurrant/irh24/Projects/FapC_VS/study/023-prep-protein-dock/data/9nqd_protonated.pdb \ 
    --ligand /ihome/jdurrant/irh24/Projects/FapC_VS/study/051-dock-pharm-div-set/data/cleaned_compounds/region_3/mol9/group_7.sdf \
    --config /ihome/jdurrant/irh24/Projects/FapC_VS/study/021-ftmap-box/data/box/region_3.txt \
    --out /ihome/jdurrant/irh24/Projects/FapC_VS/study/051-dock-pharm-div-set/data/docked_compounds/region_3/mol9/group_7.sdf \
    | tee "$LOG"
echo "Done!"
