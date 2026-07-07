# 028-pharms-top-div-set
Goal: find the pharmacophores of the most successful dockers of the diversity set

## Data
region_[]_concat.json: that region's molecules pharmacophore lists concatted together. The seperation between each molecule is just an enter, no comma. Technically invalid JSON.

## Analysis
create_pharm_get_inp: will take in all the SDFs and auto generate a slurm script to extract all pharmacophores from them
get_pharms.slurm: (output by above) uses pharmit to find pharmacophores of the SDFs input into above