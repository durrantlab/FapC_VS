#!/bin/bash

#SBATCH --job-name=023-dock-div
#SBATCH --output=bash-op.txt
#SBATCH --cluster=SMP
#time --time:1-00:


module purge
module load gnina/1.3.0

cpptraj cpp/export_prsa2-llo-ph5-r1_op.cpp
cpptraj cpp/export_prsa2-llo-ph5-r2_op.cpp
cpptraj cpp/export_prsa2-llo-ph5-r3_op.cpp

cpptraj cpp/export_prsa2-llo-ph7-r1_op.cpp
cpptraj cpp/export_prsa2-llo-ph7-r2_op.cpp
cpptraj cpp/export_prsa2-llo-ph7-r3_op.cpp
echo "done"
