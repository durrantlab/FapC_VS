# z01-create-pharm-db (SECTION SKIPPED)
~~Goal: create a pharmit database so a pharmacophore search can be done on it~~

## Data
*As it is too large, it is held in ix. Under FapC_VS/032-DB*

Each folder holds an input SDF turned into a pharmit database. Info can be found in the .json inside.

## Analysis
setup_dbcreate: takes in library of sdf molecules, edits files to be correct format and creates a script that (when run) will setup the database
job_list.txt: (output by above) each database creation job's arguments, each as a different line
create_db.sh: (output by above) submits the database creation batch job
create_db.slurm: batch job submission for creation pharmit databases