
# 026-compare-sets
Goal: take top 100 results from diversity set scoring. Use tanimoto coefficients to determine similarity. If similar, then go further with experimental set.
- Inputs: top SDF outputs from div set scoring in separate SDFs, experimental SDFs all in one together
- Outputs: report about top tanimoto similarity of each experimental saying which it is closest to, prints images of experimental molecules / similar to 

## How To Use:
1) Upload the experimental set
- Upload to the data of 026 on cluster
2) Determine which div set molecules the experimental set is most similar to
- All inside find_similarity
- Ensure that files point to where the best docked from diversity set large SDF files are, where the experimental set SDF file is, and the correct output directory (data of this section)
- Run it

## Data
log.txt: for each experimental compound, returns which top diversity set compound it is similar to and the tanimoto score
photos: has an image of every experimental compound and the diversity compound it is most similar to
exp_set.sdf: concat SDF with all experimental compounds

## Analysis
find_similarity: will determine the tanimoto / other similaries between each top div set and each exp set. Will create a .txt writeup file describing it
