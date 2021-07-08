#!/usr/bin/python3
# prep_data.py
# William O'Brien 07/08/2021

import pandas as pd

def prep(tt_split=.2, seed=100):
    fname = 'interim_data'
    param_data = pd.read_csv(f'../data/interim/{fname}.csv')

    # data cleaning
    try:
        param_data = param_data.drop(["ID","StudySample","HatchOffsetFromCountour", "MicroCTScan", "LayerHeight", "Machine", "Powder"], axis=1)
        print("dropped columns")
    except:
        print("already dropped columns")
    param_data.columns = ["LaserPowerHatch","LaserSpeedHatch","HatchSpacing","LaserPowerContour","EnergyDensityCalculated","Porosity"]


    # test train split, random sampling
    pct = 1 - tt_split

    train_data = param_data.sample(frac=pct, random_state=seed).reset_index()
    test_data = param_data.drop(train_data.index).sample(frac=1, random_state=seed).reset_index()

    print("\nexporting cleaned data...")
    train_data.to_csv('../data/processed/train.csv')
    test_data.to_csv('../data/processed/test.csv')

    print("\ndata preparation complete")

if __name__ == '__main__':
    prep(tt_split=.25, seed=100)
else:
    prep()