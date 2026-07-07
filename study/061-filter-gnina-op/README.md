# 025-filter-gnina-op
Goal: Go through all SDF files and find best pose for each molecule. Then for each region, order each molecule from best to worst CNN score

## Data
ranked_docked_mols.csv: holds the best score for each molecule across all conforms and regions. In order of CNN score
best_drugs: holds the top 10 molecules of each pocket (region)
- [].csv: holds the name /score of the best compounds for that region, in order
- [].sdf: holds those best compounds, in order, in 1 concatted SDF
- region_[]: holds the top 10 molecules for that region in seperate SDFs. Named in order from best to worst, indexing starts at 0

## Analysis
rank_docked: Will take in all docked molecules, determine the best pose for each (across conforms and regions) and store the score. Will then order on score and output in csv
get_top_drugs: will take in the best drugs csv, and for each region (box) it will find the top X best molecules. It will output them into a csv, a SDF together and SDFs seperately
