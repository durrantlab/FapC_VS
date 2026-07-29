
# c02-pharms-top-div-set
Goal: find the pharmacophores of the most successful dockers of the diversity set
- Inputs: top div set for each region (concat SDFs, format of region_#_concat.sdf in dir together), protonated PDB
- Outputs: each region’s top molecule of diversity sets pharmacophores in a concated JSON format. Name: /region_#_concat.json

## How To Use:
1) Create slurm script that will run pharmacophore extraction script
- All inside create_pharm_get_inp
- Check that it points to where top div set molecules are located, and the data of this section
- Run it with pixi
2) Run the generated slurm
- sbatch get_pharms.slurm
- Info on Pharmit: https://github.com/dkoes/pharmit/tree/master 

## Data
`region_<>_concat.json`: that region's molecules pharmacophore lists concatted together. The seperation between each molecule is just an enter, no comma. Technically invalid JSON.

## Analysis
[create_pharm_get_inp](/study/c02-pharms-top-div-set/analysis/create_pharm_get_inp.py): will take in all the SDFs and auto generate a slurm script to extract all pharmacophores from them
get_pharms.slurm: (output by above) uses pharmit to find pharmacophores of the SDFs input into above
