#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Exporting paths and variables..."
export FAPC_VS_LOG=True
export FAPC_VS_LOG_LEVEL=10
export FAPC_VS_STDOUT=True
export FAPC_VS_LOG_FILE_PATH="./01-protonate.log"
export pdb_inp="../../021-ftmap-box/data/9nqd.fftmap.cleared.pdb"
export pdb_op="../data/9nqd_protonated.pdb"

echo "Done!"

exec > >(tee $FAPC_VS_LOG_FILE_PATH) 2>&1

pdb_name="$(basename $pdb_inp)"
echo "Protonating $pdb_name..."
pixi run reduce -FLIP "&pdb_inp" > "$pdb_op"
echo "Done!"

