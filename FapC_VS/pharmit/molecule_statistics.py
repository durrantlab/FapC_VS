
import csv
import pickle
from pathlib import Path

import pandas as pd
import xgboost
from rdkit import Chem
from rdkit.Chem import Descriptors, FilterCatalog
from rdkit.Chem.FilterCatalog import FilterCatalogParams

import mordred
import numpy as np
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score as r2
from mordred import (
    ABCIndex,
    Aromatic,
    AtomCount,
    BalabanJ,
    BertzCT,
    BondCount,
    Calculator,
    CarbonTypes,
    Chi,
    EccentricConnectivityIndex,
    EState,
    HydrogenBond,
    McGowanVolume,
    Polarizability,
    RingCount,
    RotatableBond,
    SLogP,
    VdwVolumeABC,
    descriptors,
)


def build_pains_catalog():
    params = FilterCatalogParams()
    params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
    return FilterCatalog.FilterCatalog(params)


def calculate_logS(molecules, models_dir: Path) -> list:
    """Takes in a list of RDKIT molecules and returns
    their LogS. Index of LogS = index in moleculeslist.

    Args:
        molecules: list of RDKIT molecules to find LogS of
        models_dir: where the models are held

    Returns:
        float: list of LogS for each molecule. Index in this list =
            molecule's index in molecules list
    """
    all_generated_descriptors = generate(molecules)

    # Import pretrained models
    mlp_model_import = pickle.load(open((models_dir / "aqsolpred_mlp_model.pkl"), "rb"))
    xgboost_model_import = pickle.load(
        open((models_dir / "aqsolpred_xgb_model.pkl"), "rb")
    )

    # predict test data (MLP,XGB,RF)
    pred_mlp = mlp_model_import.predict(all_generated_descriptors)
    pred_xgb = xgboost_model_import.predict(all_generated_descriptors)
    # calculate consensus
    pred_consensus = (pred_mlp + pred_xgb) / 2

    return pred_consensus


def rank_csv_in(csv_rank_file: Path) -> list:
    with open(csv_rank_file, "r") as f:
        return [line.strip().split(",") for line in f.read().strip().split("\n")]


def main(sdf_file: Path, csv_rank_file: Path, models_dir: Path, csv_file: Path):
    """Takes in an SDF file, calculates a number of statistics, and places into a csv file

    CSV file format:


    Args:
        sdf_file: the concat SDF file with all molecules
        csv_rank_file: CSV with all molecules listed in ranked order
            Index = index in sdf_file
        models_dir: Where LogP models are stored
        csv_file: csv file location
            Will create folder if it does not exist
    """
    # read in the molecules
    molecules = Chem.SDMolSupplier(
        str(sdf_file), sanitize=True, removeHs=False, strictParsing=True
    )
    # setup molecule analysis
    logs_list: list[float] = calculate_logS(molecules, models_dir)
    pains_catalog = build_pains_catalog()
    csv_rank_list: list[list] = rank_csv_in(csv_rank_file)
    # create csv
    data: list[list] = [
        [
            "SDF Index",
            "Name",
            "LogS",
            "CNN_VS",
            "CNNaffinity",
            "CNN_Score",
            "Group",
            "Molar Mass",
            "Heavy Atoms",
            "Lig Eff",
            "PAINS Flags",
            "SMILES",
            "Soluability",
            "Notes",
        ]
    ]
    for ind, mol in enumerate(molecules):
        temp_data: list = []
        # get SDF index
        temp_data.append(ind)
        # get name
        temp_data.append(mol.GetProp("_Name").strip())
        # get LogS of molecules
        temp_data.append(logs_list[ind])
        # Get CNN score
        cnn_vs: float = float(mol.GetProp("CNN_VS").strip())
        temp_data.append(cnn_vs)
        # get CNN Affinity
        cnn_affinity: float = float(mol.GetProp("CNNaffinity").strip())
        temp_data.append(cnn_affinity)
        # get CNN Score
        temp_data.append(cnn_vs / cnn_affinity)
        # get region/mol/group
        temp_data.append(
            f"{csv_rank_list[ind+1][1]}/{csv_rank_list[ind+1][2].split('.')[0]}"
        )
        # get molar mass
        temp_data.append(Descriptors.MolWt(mol))
        # get heavy atoms
        heavy_atoms: int = mol.GetNumHeavyAtoms()
        temp_data.append(heavy_atoms)
        # get lig eff
        temp_data.append(cnn_affinity / heavy_atoms)
        # get pains flags
        flags = [m.GetDescription() for m in pains_catalog.GetMatches(mol)]
        temp_data.append(";".join(flags) if flags else "")
        # get smiles
        temp_data.append(Chem.MolToSmiles(mol))
        # if soluable
        temp_data.append(
            "ok" if logs_list[ind] > -4.5 else "predicted to be poorly soluable"
        )
        # notes
        temp_data.append("")

        data.append(temp_data)

    if not csv_file.parent.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, "w", newline="") as f:
        csv.writer(f).writerows(data)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 14:15:21 2019

@author: Murat Cihan Sorkun
"""


#mlp with 1 test set
def get_errors(y_true,y_pred):   

    err_mae=mae(y_true,y_pred)
    err_rmse=np.sqrt(mse(y_true,y_pred))
    err_r2=r2(y_true,y_pred)
        
    print("Ensemble MAE:"+str(err_mae)+" RMSE:"+str(err_rmse)+" R2:"+str(err_r2))
  
    return err_mae,err_rmse,err_r2
   

#returns mordred descriptor vector
def predefined_mordred(mol, desc_type="best", desc_names=False):
    
    calc1 = mordred.Calculator()    

    if(desc_type in ["best"]):
        calc1.register(mordred.SLogP)
        calc1.register(mordred.HydrogenBond.HBondAcceptor)
        calc1.register(mordred.HydrogenBond.HBondDonor)
        calc1.register(mordred.AtomCount.AtomCount("HeavyAtom"))
        calc1.register(mordred.TopoPSA.TopoPSA(True))
        calc1.register(mordred.RingCount.RingCount(None, False, False, None, None))
        calc1.register(mordred.BondCount.BondCount("any", False))
        
    
    if(desc_type in ["all","atom"]): 
        calc1.register(mordred.AtomCount.AtomCount("X"))
        calc1.register(mordred.AtomCount.AtomCount("HeavyAtom"))
        calc1.register(mordred.Aromatic.AromaticAtomsCount)
        

    if(desc_type in ["all","bond"]):  
        calc1.register(mordred.HydrogenBond.HBondAcceptor)
        calc1.register(mordred.HydrogenBond.HBondDonor)
        calc1.register(mordred.RotatableBond.RotatableBondsCount)  
        calc1.register(mordred.BondCount.BondCount("any", False))
        calc1.register(mordred.Aromatic.AromaticBondsCount)  
       	calc1.register(mordred.BondCount.BondCount("heavy", False))
       	calc1.register(mordred.BondCount.BondCount("single", False))
       	calc1.register(mordred.BondCount.BondCount("double", False))
        calc1.register(mordred.BondCount.BondCount("triple", False))

    if(desc_type in ["all","topological"]):      
        calc1.register(mordred.McGowanVolume.McGowanVolume)
        calc1.register(mordred.TopoPSA.TopoPSA(True))
        calc1.register(mordred.TopoPSA.TopoPSA(False))
        calc1.register(mordred.MoeType.LabuteASA)
        calc1.register(mordred.Polarizability.APol)
        calc1.register(mordred.Polarizability.BPol)
        calc1.register(mordred.AcidBase.AcidicGroupCount)
        calc1.register(mordred.AcidBase.BasicGroupCount)
        calc1.register(mordred.EccentricConnectivityIndex.EccentricConnectivityIndex)        
        calc1.register(mordred.TopologicalCharge.TopologicalCharge("raw",1))
        calc1.register(mordred.TopologicalCharge.TopologicalCharge("mean",1))
        
        
    if(desc_type in ["all","index"]): 
        calc1.register(mordred.SLogP)
        calc1.register(mordred.BertzCT.BertzCT)
        calc1.register(mordred.BalabanJ.BalabanJ)
        calc1.register(mordred.WienerIndex.WienerIndex(True))
        calc1.register(mordred.ZagrebIndex.ZagrebIndex(1,1))
        calc1.register(mordred.ABCIndex)
        
    if(desc_type in ["all","ring"]):     
        calc1.register(mordred.RingCount.RingCount(None, False, False, None, None))
        calc1.register(mordred.RingCount.RingCount(None, False, False, None, True))
        calc1.register(mordred.RingCount.RingCount(None, False, False, True, None))
        calc1.register(mordred.RingCount.RingCount(None, False, False, True, True))
        calc1.register(mordred.RingCount.RingCount(None, False, False, False, None))
        calc1.register(mordred.RingCount.RingCount(None, False, True, None, None))
       

    if(desc_type in ["all","estate"]):   
        calc1.register(mordred.EState)
        
# if desc_names is "True" returns only name list
    if(desc_names):
        name_list=[]
        for desc in calc1.descriptors:
            name_list.append(str(desc))
        return name_list
#        return list(calc1._name_dict.keys())
    else: 
        result = calc1(mol)
        return result._values
   

def generate(mols, verbose=False):
    selected_columns = [
        "nHBAcc",
        "nHBDon",
        "nRot",
        "nBonds",
        "nAromBond",
        "nBondsO",
        "nBondsS",
        "TopoPSA(NO)",
        "TopoPSA",
        "LabuteASA",
        "bpol",
        "nAcid",
        "nBase",
        "ECIndex",
        "GGI1",
        "SLogP",
        "SMR",
        "BertzCT",
        "BalabanJ",
        "Zagreb1",
        "ABCGG",
        "nHRing",
        "naHRing",
        "NsCH3",
        "NaaCH",
        "NaaaC",
        "NssssC",
        "SsCH3",
        "SdCH2",
        "SssCH2",
        "StCH",
        "SdsCH",
        "SaaCH",
        "SsssCH",
        "SdssC",
        "SaasC",
        "SaaaC",
        "SsNH2",
        "SssNH",
        "StN",
        "SdsN",
        "SaaN",
        "SsssN",
        "SaasN",
        "SsOH",
        "SdO",
        "SssO",
        "SaaO",
        "SsF",
        "SdsssP",
        "SsSH",
        "SdS",
        "SddssS",
        "SsCl",
        "SsI",
    ]

    # Test Data filter
    test_formula_list = []
    test_mordred_descriptors = []

    for mol in mols:
        mol = Chem.AddHs(mol)
        formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
        formula = formula.replace("+", "")
        formula = formula.replace("-", "")

        test_formula_list.append(formula)
        test_mordred_descriptors.append(
            predefined_mordred(mol, "all")
        )

    # get all column names
    column_names = predefined_mordred(
        Chem.MolFromSmiles("CC"), "all", True
    )

    # create Mordred desc dataframe
    test_df = pd.DataFrame(
        index=test_formula_list, data=test_mordred_descriptors, columns=column_names
    )

    # Select predefined columns by the model
    selected_data_test = test_df[selected_columns]
    selected_data_test = selected_data_test.apply(pd.to_numeric, errors="coerce")
    selected_data_test = selected_data_test.fillna(0)

    nan_cols = selected_data_test.columns[selected_data_test.isna().any()].tolist()
    if nan_cols:
        print(
            f"Warning: {len(nan_cols)} descriptors failed: {nan_cols[:5]}..."
        )  # Show first 5

    return selected_data_test
