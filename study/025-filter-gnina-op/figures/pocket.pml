set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4


delete all
load D:\\FapC_VS\\study\\001-base-data\\data\\9NQD.cif
load D:\\FapC_VS\\study\\025-filter-gnina-op\\data\\best_drugs\\region_1\\r00_F0608-0624.sdf
dss

select entire, all and not chain 3 and not chain 4
select mol, object r00_F0608-0624

hide sticks
hide cartoon
show cartoon, entire
color gray, entire
color yellow, mol


center residue 1000, -1
set_view (\
    -0.401487559,   -0.090677358,   -0.911362767,\
     0.915598452,   -0.063578732,   -0.397020280,\
    -0.021938782,   -0.993835509,    0.108547471,\
    -0.001256689,    0.001078886, -211.774826050,\
   106.790054321,  110.942901611,   50.433795929,\
    71.392059326,  352.371276855,  -20.000000000 )

ray
png pocket.png