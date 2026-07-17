
# e02-pharms-exp-set
Goal: find the pharmacophores of the experimental set
- Inputs: protonated PDB, experimental set (single SDF with all experimental molecules present)
- Outputs: each molecule in experimental sets list of pharmacophores, together in a concat JSON

## How To Use:
1) Create slurm script that will run pharmacophore extraction script
- All inside create_pharm_get_inp
- Check that it points to where top div set molecules are located, and the data of this section
- Run it with pixi
2) Submit the generated slurm
- sbatch get_pharms.slurm

## Data
exp_set.json: all experimental molecule's pharmacophore lists concatted together. The seperation between each molecule is just an enter, no comma. Technically invalid JSON.

## Analysis
create_pharm_get_inp.py: will take in all the SDFs and auto generate a slurm script to extract all pharmacophores from them
get_pharms.slurm: (output by above) uses pharmit to find pharmacophores of the SDFs input into above
