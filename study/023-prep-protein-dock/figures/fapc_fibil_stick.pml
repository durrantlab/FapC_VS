set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4


delete all
load D:\\FapC_VS\\study\\023-prep-protein-dock\\data\\9nqd_protonated.pdb
dss

select single, chain A
select entire, all

hide sticks
show cartoon
show sticks, single
color gray, entire
util.cnc("single",_self=cmd)

center residue 1000, -1

set_view (\
     0.661389172,   -0.150871322,    0.734710634,\
    -0.744999409,   -0.018758625,    0.666790187,\
    -0.086819544,   -0.988361657,   -0.124801904,\
     0.001101144,    0.000401453,  -84.395729065,\
    78.533470154,  134.695159912,   28.779064178,\
   -56.554725647,  224.424392700,  -20.000000000 )

ray
png fapc_fibril_stick.png