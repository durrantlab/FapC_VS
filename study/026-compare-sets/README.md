# 026-compare-sets
Goal: take top results from diversity set scoring. Uses tanimoto to determine similarity.
- Inputs: top SDF outputs from div set scoring, experimental SDFs
- Outputs: report about top tanimoto similarity of each experimental and which div it is to


## Data
log.txt: for each experimental compound, returns which top diversity set compound it is similar to and the tanimoto score
photos: has an image of every experimental compound and the diversity compound it is most similar to

## Analysis
find_similarity: will determine the tanimoto / other similaries between each top div set and each exp set. Will create a .txt writeup file describing it