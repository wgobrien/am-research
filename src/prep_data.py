#!/usr/bin/python3
# prep_data.py
# William O'Brien

import pandas as pd

def prep():
    fname = 'interim_data'
    param_data = pd.read_csv(f'../data/interim/{fname}.csv')

    try:
        param_data = param_data.drop(["ID","StudySample","HatchOffsetFromCountour", "MicroCTScan", "LayerHeight", "Machine", "Powder"], axis=1)
        print("dropped columns")
    except:
        print("already dropped columns")
    param_data.columns = ["LaserPowerHatch","LaserSpeedHatch","HatchSpacing","LaserPowerContour","EnergyDensityCalculated","Porosity"]
    param_data.head()

    split_pct = .25
    seed = 100

    train_data = param_data.sample(frac=split_pct, random_state=seed)
    test_data = param_data.drop(train_data.index)

    print("\nexporting cleaned data...")
    train_data.to_csv('../data/processed/train.csv')
    test_data.to_csv('../data/processed/test.csv')

    print("\ndata preparation complete")

if __name__ == '__main__':
    prep()