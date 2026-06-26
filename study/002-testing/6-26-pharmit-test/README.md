# 6-26-pharmit-test
Goal: determine why pharmit is not returning valid compounds

## Test 1: Single Molecule in Current DB (one)
Put in a single pharamacophore list (region1, mol1, all) into DB search of just 000-000 DB

Result: the top molecule was 0,0.12844677,531,9,mol_i0058211,58211,3814916096. Looked reasonable.
The molport code is: https://www.molport.com/shop/compound/Molport-000-072-206. Looks same as found molecule
 - ISSUE 1: the SDF names are just the indicies in the file. Should change to be file name + molport name.
Molecule was not found in online search

Conclusion: it seems that at least 000-000 DB is working / searching with 1 DB might be working.


## Test 2: Single Molecule in Current DB (tw0)
Put in a single pharamacophore list (region1, mol1, all) into DB search of just 000-000 DB and 000-500

Result: top molecule was now 0,0.12539689,520,13,mol_i0534473,68947,4518445057 (second was above)
Molport is: https://www.molport.com/shop/compound/Molport-000-918-948

Conclusion: 000-500 DB is working/ searching with 2 DB might be working



## Test 3: Single Molecule in Current DB (All)
Put in a single pharamacophore list (region1, mol1, all) into DB search of just 000-000 DB and 000-500

Result: top molecule name / RMSD is still the same: 0,0.12539689,520,13,mol_i0534473,448150,29369892865
however, the molecule in SDF is now cursed again

Conclusion: all DBs together do NOT work. Is it a specific database curropting? Or is multiple databases in one
query not a feature?


## Test 4: Single Molecule in Current DB (All, but seperate)
Put in a single pharamacophore list (region1, mol1, all) into DB search of each DB by itself.

Result: overall they looked good, even weird ones, were weird on the website too.

Conclusion: all DBs seperate seem to work. Will do that from now on.