#!/usr/bin/python3
# prep_data.py
# William O'Brien 07/08/2021

import pandas as pd
import os

def prep(tt_split=.2, seed=100):
    print("--------------------\nProcessing Data\n--------------------")

    # reading in transformed csv data from interim - EDIT fname as needed or read in additional files for cleaning
    fname = 'interim_data'
    f = os.path.join(os.path.dirname(__file__), f'../data/interim/{fname}.csv')
    param_data = pd.read_csv(f)

    # ---------------------------------------------------------------------------
    # data cleaning - EDIT here for custom processing, use Jupyter notebooks as scratch to ensure you are getting expected output and to save dev time

    drop_cols = ["ID","StudySample","HatchOffsetFromCountour", "LaserPowerCountour","HatchSpacing", "MicroCTScan", "Machine", "Powder","LayerHeight"]
    for col in drop_cols:
        try:
            # dropping unnecessary columns, put into error catching so the program doesn't quit if one of these are already dropped or doesnt exist
            param_data = param_data.drop(col, axis=1)
            print(f"dropped {col}")
        except:
            print(f"already dropped {col}")
    try:
        # dropping outliers
        param_data = param_data.drop([10,14,9], axis=0).reset_index(drop=True)
    except:
        print('already dropped outliers')

    # reorder to put label (Porosity) to make label selection easy (can index last column with [:,-1])
    param_data = param_data[["LaserPowerHatch","LaserSpeedHatch","EnergyDensityCalculated","Porosity"]]
    
    # show data in pipeline
    print('\n')
    print(param_data.head())

    # ------------------------------------------------------------------------
    # test train split, random sampling, train/test exports - can be left alone
    pct = 1 - tt_split

    train_data = param_data.sample(frac=pct, random_state=seed).reset_index(drop=True)
    test_data = param_data.drop(train_data.index).sample(frac=1, random_state=seed).reset_index(drop=True)

    print("\nexporting cleaned data...")
    f_train = os.path.join(os.path.dirname(__file__), '../data/processed/train.csv')
    train_data.to_csv(f_train, index=False)
    
    f_test = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test_data.to_csv(f_test, index=False)

    print("\ndata preparation complete")

if __name__ == '__main__':
    prep(tt_split=.25, seed=100)
else:
    prep()