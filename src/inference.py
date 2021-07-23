#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
from tensorflow import keras
import joblib
import os

def infer():
    print("--------------------\nInference & Scoring\n--------------------")

    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X = test_vals[:,:-2]
    y = test_vals[:,-1]

    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # load and score models

    svr1_path = os.path.join(models_path, 'svr_model1.jl')
    SVR1 = joblib.load(svr1_path)
    SVR1_score = SVR1.score(X, y)

    mlp_path = os.path.join(models_path, 'mlp_regressor.jl')
    MLP = joblib.load(mlp_path)
    MLP_score = MLP.score(X, y)

    nn_path = os.path.join(models_path, 'nn_model.h5')
    nn = keras.models.load_model(nn_path)
    nn_score = nn.evaluate(X,y)

    # change parameters to energy density
    X = test_vals[:,-2].reshape(-1,1)
    
    svr2_path = os.path.join(models_path, 'svr_model2.jl')
    SVR2 = joblib.load(svr2_path)
    SVR2_score = SVR2.score(X, y)
    print(MLP.predict([[300,1200]]))
    
    print('---------------------')
    print('SVR Score:', SVR1_score)
    print('SVR Score Energy Density:', SVR2_score)
    print('MLP Score:', MLP_score)
    print('NN Score:', nn_score)
    print('---------------------')

if __name__ == '__main__':
    infer()