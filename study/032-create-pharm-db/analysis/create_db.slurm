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

pixi run -e pharmit pharmit dbcreate -dbdir /ihome/jdurrant/irh24/Projects/FapC_VS/study/032-create-pharm-db/data/DB -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-000-000-000--000-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-000-500-000--000-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-001-000-000--001-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-001-500-000--001-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-002-000-000--002-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-002-500-000--002-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-003-000-000--003-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-003-500-000--003-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-004-000-000--004-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-004-500-000--004-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-005-000-000--005-499-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-005-500-000--005-999-999.sdf -in /ihome/jdurrant/irh24/Projects/molport_cmpds/iis-006-000-000--006-499-999.sdf