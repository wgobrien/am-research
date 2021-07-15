#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.neural_network import MLPRegressor
from sklearn import svm
import pickle
import os

def train():

    print("--------------------\nTraining Models\n--------------------")

    fpath = '../data/processed/train.csv'
    f_train = os.path.join(os.path.dirname(__file__), fpath)
    train = pd.read_csv(f_train)
    train_vals = train.values
    
    # hard coded columns for parameter selection

    # -----------------------------------------------------------------
    # LaserPowerHatch, LaserSpeedHatch, HatchSpacing, LaserPowerContour
    X = train_vals[:,1:-2]
    y = train_vals[:,-1]

    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model1 = svm.SVR(kernel='poly', degree=2)
    svr_model1.fit(X, y)
    # Multi-layer Perceptor ANN 
    mlp_regressor = MLPRegressor(hidden_layer_sizes=5, activation='logistic', solver='lbfgs')
    mlp_regressor.fit(X, y)
    # NEURAL NETWORK
    nn_model = keras.models.Sequential([
        keras.layers.Dense(5),
        keras.layers.Dense(1)
    ])

    nn_model.compile()
    nn_model.fit()
    
    # -----------------------------------------------------------------
    # EnergyDensityCalculated
    X = train_vals[:,-2].reshape(-1,1)
    
    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model2 = svm.SVR(kernel='poly', degree=2)
    svr_model2.fit(X, y)

    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    pickle.dump(svr_model1, open(os.path.join(models_path, 'svr_model1.sav'), 'wb'))
    pickle.dump(svr_model2, open(os.path.join(models_path, 'svr_model2.sav'), 'wb'))
    pickle.dump(mlp_regressor, open(os.path.join(models_path, 'mlp_regressor.sav'), 'wb'))

    print('models built successfully.')

if __name__ == '__main__':
    train()
