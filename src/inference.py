#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
from sklearn import model_selection
import pickle

def infer():

    # read in test data, split parameters and labels
    test = pd.read_csv('../data/processed/test.csv')
    test_vals = test.values
    
    X = test_vals[:,1:-1]
    y = test_vals[:,:-2:-1].T[0]

    # load and score models
    LR1 = pickle.load(open('../models/lr_model1.sav', 'rb'))
    LR1_score = LR1.score(X, y)

    SVR1 = pickle.load(open('../models/svr_model1.sav', 'rb'))
    SVR1_score = SVR1.score(X, y)

    X = test_vals[:,-2:-1]
    LR2 = pickle.load(open('../models/lr_model2.sav', 'rb'))
    LR2_score = LR2.score(X, y)

    print('LR Score:', LR1_score)
    print('LR Score Energy Density:', LR2_score)
    print('SVR Score:', SVR1_score)

    print('---------------------\n')

    print(SVR1.get_params())

if __name__ == '__main__':
    infer()