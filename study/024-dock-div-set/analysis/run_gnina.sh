sbatch --array=0-$((N-1))  \
       --export=ALL   \
       ../structures/protein/dock.slurm