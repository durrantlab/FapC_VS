set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4


delete all
load D:\\FapC_VS\\study\\001-base-data\\data\\9NQD.cif
load D:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_1\\r01_F3382-4604.sdf
dss

select entire, all and not chain 3 and not chain 4
select mol, object r01_F3382-4604

hide sticks
hide cartoon
show sticks, mol
color gray, entire
color cyan, mol


center residue 1000, -1
set_view (\
    -0.401487559,   -0.090677358,   -0.911362767,\
     0.915598452,   -0.063578732,   -0.397020280,\
    -0.021938782,   -0.993835509,    0.108547471,\
    -0.001337133,    0.000917383,  -89.342132568,\
   100.516876221,  123.602111816,   45.678016663,\
   -50.865703583,  230.113525391,  -20.000000000 )

ray
png drug_r1_91.png