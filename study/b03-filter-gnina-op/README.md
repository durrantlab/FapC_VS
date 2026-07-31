
# b03-filter-gnina-op
Goal: Go through all SDF files and find best pose (based on CNN_VS) for each molecule. Then for each region, find top 10 molecules from best to worst
-   Input: Docked molecules in large SDF files with CNN_VS scores listed from gnina. Organized /region_#/ligs_##.sdf
-   Output: CSV that holds best variant of each molecule (across regions and poses), ordered best to worst. The best molecules for each region all in separate SDFs, a concat SDF, and a CSV.

## How To Use:
1)  Determine the best pose for each molecule and rank off of its CNN_VS score in a csv
-   Check that rank_docked script points to Gnina outputs, and CSV points to this sections data
-   Run
1)  Extract the top ten poses for each box
-   In get_top_drugs, see if it points to docked SDFs, the csv_rank file from previous and best_drugs directory to place all outputs
-   Also check that the # of top molecules to take is 10
-   Then run get_top_drugs
1)  Analyze the poses, sanity check
-   From 025 download docked, concatted ligands
-   From 023 download protonated protein
-   Open them all up, look through, and save to visualization file

## Data
ranked_docked_mols.csv: for each compound's best pose/region holds: cnn_vs,directory,file_name,pose_ind,name. Sorted based on CNN_VS
best_drugs: holds the top 10 molecules of each pocket (region)
-   `<>.csv`: for top compounds of region holds: cnn_vs,directory,file_name,pose_ind,name. Sorted based on CNN_VS
-   `<>.sdf`: holds those best compounds, in order, in 1 concatted SDF
-   `region_<>`: holds the top 10 molecules for that region in seperate SDFs. Named in order from best to worst, indexing starts at 0

## Analysis
[rank_docked](/study/b03-filter-gnina-op/analysis/rank_docked.py): Will take in all docked molecules, determine the best pose for each (across conforms and regions) and store the score. Will then order on score and output in csv
[get_top_drugs](/study/b03-filter-gnina-op/analysis/get_top_drugs.py): will take in the best drugs csv, and for each region (box) it will find the top X best molecules. It will output them into a csv, a SDF together and SDFs seperately
