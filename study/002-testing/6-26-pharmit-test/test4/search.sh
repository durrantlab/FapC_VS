pixi run -e pharmit pharmit dbsearch -max-weight 750 \
    -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output0.sdf \
    -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-000-000-000--000-499-999 \
    > output0.txt
pixi run -e pharmit pharmit dbsearch -max-weight 750 \
    -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output1.sdf \
    -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-000-500-000--000-999-999 \
    > output1.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 \
    -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output2.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-002-500-000--002-999-999 \
    > output2.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 \
    -extra-info -sort-rmsd -in reg_1_mol1_base_input.json \
    -out reg_1_mol1_base_output3.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-005-000-000--005-499-999 \
    > output3.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 \
    -extra-info -sort-rmsd -in reg_1_mol1_base_input.json \
    -out reg_1_mol1_base_output4.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-003-000-000--003-499-999 \
    > output4.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output5.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-005-500-000--005-999-999 \
    > output5.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output6.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-001-000-000--001-499-999 \
    > output6.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output7.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-003-500-000--003-999-999 \
    > output7.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output8.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-006-000-000--006-499-999 \
    > output8.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output9.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-001-500-000--001-999-999 \
    > output9.txt
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output10.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-004-000-000--004-499-999 \
    > output10.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output11.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-002-000-000--002-499-999 \
    > output11.txt 
pixi run -e pharmit pharmit dbsearch -max-weight 750 -extra-info -sort-rmsd \
    -in reg_1_mol1_base_input.json -out reg_1_mol1_base_output12.sdf -max-hits 2000 \
    -dbdir /ix/jdurrant/durrantlab/irh24/FapC_VS/032-DB/iis-004-500-000--004-999-999 \
    > output12.txt