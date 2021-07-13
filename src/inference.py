#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
import pickle
import os

def infer():

    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X = test_vals[:,1:-2]
    y = test_vals[:,-1]

    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # load and score models

    svr1_path = os.path.join(models_path, 'svr_model1.sav')
    SVR1 = pickle.load(open(svr1_path, 'rb'))
    SVR1_score = SVR1.score(X, y)

    mlp_path = os.path.join(models_path, 'mlp_regressor.sav')
    MLP = pickle.load(open(mlp_path, 'rb'))
    MLP_score = MLP.score(X, y)

    # change parameters to energy density
    X = test_vals[:,-2].reshape(-1,1)
    
    svr2_path = os.path.join(models_path, 'svr_model2.sav')
    SVR2 = pickle.load(open(svr2_path, 'rb'))
    SVR2_score = SVR2.score(X, y)
    
    print('---------------------')
    print('SVR Score:', SVR1_score)
    print('SVR Score Energy Density:', SVR2_score)
    print('MLP Score:', MLP_score)
    print('---------------------')

if __name__ == '__main__':
    infer()