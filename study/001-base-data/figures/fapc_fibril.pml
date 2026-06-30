set ambient, 0.25
set cartoon_transparency, 0.35
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4


delete all
load D:\\FapC_VS\\study\\001-base-data\\data\\9NQD.cif
dss

select single, chain 3
select entire, all

hide sticks
show cartoon
color gray, entire
color cyan, single


center residue 1000, -1

PyMOL>get_view
### cut below here and paste into script ###
set_view (\
     0.753155410,   -0.044869974,    0.656307697,\
    -0.656338155,    0.016160252,    0.754284680,\
    -0.044452693,   -0.998848736,   -0.017275086,\
     0.000524402,    0.002120554, -653.389648438,\
   108.709968567,  110.965362549,  101.286209106,\
   512.878173828,  793.857299805,  -20.000000000 )

ray
png test.png