@load_fapc.pml

select single, chain 3
select entire, all

hide sticks
hide cartoon
show cartoon, single
color cyan, single


center residue 1000, -1

set_view (\
     0.753187001,   -0.044336606,    0.656307697,\
    -0.656349421,    0.015695453,    0.754284680,\
    -0.043745331,   -0.998879969,   -0.017275086,\
     0.000541128,    0.000258207, -194.014709473,\
   107.165351868,  110.576927185,   28.621614456,\
    53.451919556,  334.430847168,  -20.000000000 )

ray
png fapc_monomer.png