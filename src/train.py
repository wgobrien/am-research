#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
from sklearn.neural_network import MLPRegressor
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
    X = train_vals[:,1:-2]
    y = train_vals[:,-1]

    svr_model1 = svm.SVR(kernel='poly', degree=2)
    svr_model1.fit(X, y)

    mlp_regressor = MLPRegressor(hidden_layer_sizes=5, activation='logistic', solver='lbfgs')
    mlp_regressor.fit(X, y)

    # EnergyDensityCalculated
    X = train_vals[:,-2].reshape(-1,1)
    
    svr_model2 = svm.SVR(kernel='poly', degree=2)
    svr_model2.fit(X, y)

    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    pickle.dump(svr_model1, open(os.path.join(models_path, 'svr_model1.sav'), 'wb'))
    pickle.dump(svr_model2, open(os.path.join(models_path, 'svr_model2.sav'), 'wb'))
    pickle.dump(mlp_regressor, open(os.path.join(models_path, 'mlp_regressor.sav'), 'wb'))

    print('models built successfully.')

if __name__ == '__main__':
    train()
