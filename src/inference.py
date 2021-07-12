#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle
import os

def infer():

    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X = test_vals[:,1:-1]
    y = test_vals[:,:-2:-1].T[0]

    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # load and score models
    lr1_path = os.path.join(models_path, 'lr_model1.sav')
    LR1 = pickle.load(open(lr1_path, 'rb'))
    LR1_score = LR1.score(X, y)

    svr1_path = os.path.join(models_path, 'svr_model1.sav')
    SVR1 = pickle.load(open(svr1_path, 'rb'))
    SVR1_score = SVR1.score(X, y)

    # change parameters to energy density
    #X = test_vals[:,-2:-1]
    
    #lr2_path = os.path.join(models_path, 'lr_model2.sav')
    #LR2 = pickle.load(open(lr2_path, 'rb'))
    #LR2_score = LR2.score(X, y)
    
    print('---------------------')
    print('LR Score:', LR1_score)
    #print('LR Score Energy Density:', LR2_score)
    print('SVR Score:', SVR1_score)
    print('SVR MSE:', mean_squared_error(y, SVR1.predict(X)))
    print('---------------------')

if __name__ == '__main__':
    infer()