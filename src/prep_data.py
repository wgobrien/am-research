#!/usr/bin/python3
# prep_data.py
# William O'Brien 07/08/2021

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import StandardScaler, MinMaxScaler

def prep(tt_split=.25, seed=100):
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
    print()
    print(param_data.head())

    # ------------------------------------------------------------------------
    # test train split, random sampling, train/test exports - can be left alone
    pct = 1 - tt_split

    train_data = param_data.sample(frac=pct, random_state=seed).reset_index(drop=True)
    test_data = param_data.drop(train_data.index).sample(frac=1, random_state=seed).reset_index(drop=True)

    # scale data and export scaler models
    train_data, test_data, sx, sy = transform(train_data, test_data, MinMaxScaler(), StandardScaler())
    models_path = os.path.join(os.path.dirname(__file__), '../models/scalers')

    joblib.dump(sx, os.path.join(models_path,'X_scale.pkl'))
    joblib.dump(sy, os.path.join(models_path,'y_scale.pkl'))

    print("\nexporting cleaned data...")
    f_train = os.path.join(os.path.dirname(__file__), '../data/processed/train.csv')
    train_data.to_csv(f_train, index=False)
    
    f_test = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test_data.to_csv(f_test, index=False)

    print("\ndata preparation complete")


def feature_label_join(X, y):
    df = pd.DataFrame(np.concatenate([X,y], axis=1))
    df.columns = ['LaserPowerHatch', 'LaserSpeedHatch', 'EnergyDensity', 'Porosity']
    return df


def transform(train_data, test_data, scale_X, scale_y):
    train_vals = train_data.values
    test_vals = test_data.values

    X_train = scale_X.fit_transform(train_vals[:,:-1])
    y_train = scale_y.fit_transform(train_vals[:,-1].reshape(-1, 1))

    X_test = scale_X.transform(test_vals[:,:-1])
    y_test = scale_y.transform(test_vals[:,-1].reshape(-1, 1))

    train = feature_label_join(X_train, y_train)
    test = feature_label_join(X_test, y_test)

    return train, test, scale_X, scale_y


if __name__ == '__main__':
    prep(tt_split=.25, seed=100)
else:
    prep()