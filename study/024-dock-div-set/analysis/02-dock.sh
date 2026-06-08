#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Exporting paths and variables..."
export PSMA1_VS_LOG=True
export PSMA1_VS_LOG_LEVEL=10
export PSMA1_VS_STDOUT=True
export PSMA1_VS_LOG_FILE_PATH="./02-docking.log"
export PROTEIN_DIR="../structures/protein"
export LIGAND_FILE="../structures/compounds/top_ligands.sdf"
export JOB_LIST="${PROTEIN_DIR}/job_list.txt"
echo "Done!"

echo "Creating job list file for all jobs..."
> "$JOB_LIST"

echo "Looking for all protein receptors and creating the array..."
RECEPTORS=$(find "$PROTEIN_DIR" -name "*protonated.pdb" | sort )
echo "Done!"

echo "Looking for all config files for each receptor and creating the array..."
for receptor in $RECEPTORS;
  do
  DIR_NAME=$(dirname "$receptor")
  for config in $(find "$DIR_NAME" -name "*.txt" | sort);
  do
    RECEPTOR_NAME=$(basename "$receptor" "_protonated.pdb")
    CONFIG_NAME=$(basename "$config" ".txt")
    OUT="${DIR_NAME}/${RECEPTOR_NAME}_${CONFIG_NAME}_docked.sdf"
    echo "Making the command for $RECEPTOR_NAME and $CONFIG_NAME..."
    echo "--receptor $receptor --ligand $LIGAND_FILE --config $config --out $OUT" >> "$JOB_LIST"
    echo "Done!"
  done
done
echo "Done!"

echo "Counting number of jobs in job array..."
N=$(wc -l < "$JOB_LIST")
echo "Done! Found $N jobs."

sbatch --array=0-$((N-1))  \
       --export=ALL   \
       ../structures/protein/dock.slurm
