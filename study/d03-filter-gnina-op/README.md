
# d03-filter-gnina-op
Goal: Go through each docked molecule and find best pose. Then order from best to worst
- Input: Docked molecules in large SDF files with CNN_VS scores listed from gnina. Organized /region_#/mol#/group_#.sdf
- Output: the best overall molecules all in separate SDFs, a concatenated SDF, and a CSV

## How To Use:
1) For each region / mol: determine the best pose for each molecule and rank off of its CNN_VS score in a csv
- Check that rank_docked script points to Gnina outputs, and CSV points to this sections data
- Run
2) Check: pose ranking / molecule ranking
- See that the top pose for a molecule actually is the best
- See that the top molecules are actually top
3) Extract the top hundred poses
- In get_top_drugs, see if it points to docked SDFs, the csv_rank file from previous and best_drugs directory to place all outputs
- Make sure # of top molecules to take is 100
- Then run get_top_drugs
4) Check: molecule extraction
- Check extracted molecules are top 100. Both in concat and in single

## Data
ranked_docked_mols.csv: holds the best score for each molecule across all conforms. In order of CNN_VS score
best_drugs: holds the top 100 molecules
- [].csv: holds the name / location / score of the best compounds for that region, in order of CNN_VS. cnn_vs,directory,file_name,pose_ind,name
- [].sdf: holds those best compounds, in order, in 1 concatted SDF
- singles: holds the top 100 molecules in seperate SDFs. Named in order from best to worst, indexing starts at 0. r#_[name of molecule].sdf

## Analysis
rank_docked: Will take in all docked molecules, determine the best pose for each (across conforms) and store the score. Will then order on score and output in csv
get_top_drugs: will take in the best drugs csv, and find the top X best molecules. It will output them into a csv, a SDF together and SDFs seperately
