#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import svm
import pickle
import os

def train():

    print('training models...')

    fpath = '../data/processed/train.csv'
    f_train = os.path.join(os.path.dirname(__file__), fpath)
    train = pd.read_csv(f_train)

    train_vals = train.values
    
    # hard coded columns for parameter selection

    # LaserPowerHatch, LaserSpeedHatch, HatchSpacing, LaserPowerContour
    X = train_vals[:,1:-1]
    y = train_vals[:,:-2:-1].T[0]
    
    lr_model1 = LinearRegression()
    lr_model1.fit(X, y)

    svr_model1 = svm.SVR()
    svr_model1.fit(X, y)

    # EnergyDensityCalculated
    X = train_vals[:,-2:-1]
    
    lr_model2 = LinearRegression()
    lr_model2.fit(X, y)

    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    pickle.dump(lr_model1, open(os.path.join(models_path, 'lr_model1.sav'), 'wb'))
    pickle.dump(svr_model1, open(os.path.join(models_path, 'svr_model1.sav'), 'wb'))
    pickle.dump(lr_model2, open(os.path.join(models_path, 'lr_model2.sav'), 'wb'))

    print('models built successfully.')

if __name__ == '__main__':
    train()