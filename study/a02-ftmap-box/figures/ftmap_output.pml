set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4

delete all
load ../data/9nqd.fftmap.output.pdb
dss

select entire, protein

show sticks
hide sticks, entire
show cartoon, entire
color gray, entire


set_view (\
     0.236147180,   -0.043538526,   -0.970740795,\
    -0.971699178,   -0.004417891,   -0.236181945,\
     0.005993601,    0.999041975,   -0.043349702,\
     0.000000000,    0.000000000, -245.405136108,\
   100.925071716,  106.901550293,   41.934860229,\
   193.479278564,  297.330993652,  -20.000000000 )
ray
png ftmap_output.png

