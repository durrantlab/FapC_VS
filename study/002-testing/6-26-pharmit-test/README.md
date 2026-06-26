# 6-26-pharmit-test
Goal: determine why pharmit is not returning valid compounds

## Test 1: Single Molecule in Current DB
Put in a single pharamacophore list (region1, mol1, all) into DB search of just 000-000 DB

Result: the top molecule was 0,0.12844677,531,9,mol_i0058211,58211,3814916096. Looked reasonable.
The molport code is: https://www.molport.com/shop/compound/Molport-000-072-206. Looks same as found molecule
 - ISSUE 1: the SDF names are just the indicies in the file. Should change to be file name + molport name.
Molecule was not found in online search

Conclusion: it seems that at least 000-000 DB is working / searching with 1 DB might be working.