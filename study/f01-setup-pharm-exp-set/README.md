
# f01-setup-pharm-exp-set
Goal: take the set of molecules similar to experimental set and set them up with gypsum.
- Input: many similar molecules for each molecule in experimental set. Will be a folder with 1 SDF for each experimental molecule. /mol#.sdf
- Output: a folder for each molecule, has multiple SDFs each with up to 250 molecules setup in it. /mol#/group_#/[].sdf. 20 groups in total (5000/250 = 20)

## How To Use:
1) Run gypsum on the molecules
- Create gypsum input scripts running setup_gypsum_run
 - Check the paths are correct
 - Run with pixi
- Run gypsum
 - chmod +x run_gypsum.sh
 - ./run_gypsum.sh
2) Sanity check: split
- Check that the start and end of group_0 for a specific mol line up with molecule 0 and 249
- Check that start of group_1 is molecule 250
- Check that end of group_x is molecule 4999
3) Sanity check: gypsum
- Check that start / end of a group is the same molecule as in the split file of the same group
- Check that all groups are successful by rerunning setup_gypsum and seeing if anything is in job_list.txt

## Data
split_sdf/ holds all similar molecules, but for each /mol#, it is split into groups so each SDF has 250 (so 8 groups / molecule)
- region_#/mol#/group_#.sdf
output_sdf/ holds all similar molecules, now setup with gypsum. Organization: region_#/mol#/group_#/[].sdf

## Analysis
setup_gypsum.py: Takes in all the SDF to be gypsumed, splits into X chunks, then creates gypsum inputs to be run
run_gypsum.sh: submits the batch jobs (created)
run_gypsum.slurm: settings for the batch job
job_list.txt: list of arguments for each run of gypsum (created)
