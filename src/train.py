#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import matplotlib.pyplot as plt
import joblib
import os


def train():

    print("--------------------\nTraining Models\n--------------------")

    fpath = '../data/processed/train.csv' # train.csv file path from src
    f_train = os.path.join(os.path.dirname(__file__), fpath) # objective file path to data
    train = pd.read_csv(f_train) # read in training data
    train_vals = train.values # convert pandas dataframe to numpy matrix
    
    # hard coded columns for parameter selection
    # -----------------------------------------------------------------
    # LaserPowerHatch, LaserSpeedHatch, HatchSpacing, LaserPowerContour
    X = train_vals[:,:-2]
    y = train_vals[:,-1]

    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model1 = svm.SVR(kernel='poly', degree=2)
    svr_model1.fit(X, y)
    
    ## Multi-layer Perceptor ANN 
    mlp_regressor = MLPRegressor(hidden_layer_sizes=(5,), activation='logistic', solver='lbfgs')
    mlp_regressor.fit(X, y)

    ## NEURAL NETWORK
    nn_model = Sequential([
        Dense(5,input_shape=X.shape[1:],activation='relu'),
        Dense(1, activation='linear')
    ])

    nn_model.compile(loss='mse', optimizer='sgd')
    nn_hist = nn_model.fit(X, y, epochs=20, batch_size=5)
    
    # -----------------------------------------------------------------
    # EnergyDensityCalculated
    X = train_vals[:,-2].reshape(-1,1)
    
    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model2 = svm.SVR(kernel='poly', degree=2)
    svr_model2.fit(X, y)


    vis = input('show neural net training history [y/n]? ')
    if vis == 'y' or vis == 'yes':
        pd.DataFrame(nn_hist.history).plot(figsize=(12,8))
        plt.grid(True)
        plt.gca().set_ylim(0,1) # set y axis range [0,1]
        plt.show()
    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    joblib.dump(svr_model1, os.path.join(models_path, 'svr_model1.pkl'))
    joblib.dump(svr_model2, os.path.join(models_path, 'svr_model2.pkl'))
    joblib.dump(mlp_regressor,os.path.join(models_path, 'mlp_regressor.pkl'))
    nn_model.save(os.path.join(models_path, 'nn_model.h5'))

    print('models exported successfully.')

if __name__ == '__main__':
    train()
