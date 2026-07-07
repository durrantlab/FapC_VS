set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4


delete all
load F:\\FapC_VS\\study\\023-prep-protein-dock\\data\\9nqd_protonated.pdb
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_1\\r01_F3382-4604.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_1\\r03_F5231-0075.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_1\\r08_F3165-1168.sdf

load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_2\\r00_F3394-0291.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_2\\r07_F3394-0637.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_2\\r09_F0192-0171.sdf

load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_3\\r00_F5012-0253.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_3\\r04_F8887-2343.sdf
load F:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_3\\r09_F3407-0812.sdf


dss

select mols, not object 9nqd_protonated
select r1, object r01_F3382-4604 or object r03_F5231-0075 or object r08_F3165-1168
select r2, object r00_F3394-0291 or object r07_F3394-0637 or object r09_F0192-0171
select r3, object r00_F5012-0253 or object r04_F8887-2343 or object r09_F3407-0812
select protein, object 9nqd_protonated


hide sticks
hide cartoon

show cartoon, protein
color gray, protein

show sticks, mols
color cyan, r1
color orange, r2
color green, r3



center residue 1000, -1
set_view (\
     0.846312165,   -0.143275440,    0.513055742,\
    -0.526293278,   -0.076092035,    0.846884847,\
    -0.082299151,   -0.986739039,   -0.139797240,\
     0.000241517,    0.000869408, -232.528015137,\
   106.890777588,  109.999221802,   39.641635895,\
    92.324111938,  373.303283691,  -20.000000000 )

ray
png all_drugs.png