#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
from tensorflow.keras import layers
from tensorflow.keras import models
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import joblib
import os


def train_nn():
    print("--------------------\nTraining NN Models\n--------------------")

    fpath = '../data/processed/train.csv' # train.csv file path from src
    f_train = os.path.join(os.path.dirname(__file__), fpath) # objective file path to data
    train = pd.read_csv(f_train) # read in training data
    train_vals = train.values # convert pandas dataframe to numpy matrix

    # -----------------------------------------------------------------
    # LaserPowerHatch, LaserSpeedHatch, HatchSpacing, LaserPowerContour
    X = train_vals[:,:-2]
    y = train_vals[:,-1]

    # ----------------------------------------------------------------- 
    # NN Model Builds

    ## Sklearn Multi-layer Perceptor ANN 
    mlp_regressor = MLPRegressor(hidden_layer_sizes=(5,), activation='logistic', solver='lbfgs')
    mlp_regressor.fit(X, y)

    ## TF ANN
    input = layers.Input(shape=X.shape[1:])
    h1 = layers.Dense(5, activation='relu')(input)
    h2 = layers.Dense(5, activation='relu')(h1)
    concat = layers.Concatenate()([input, h2])
    out = layers.Dense(1)(concat)
    nn_model = models.Model(inputs=[input], outputs=[out])

    nn_model.compile(loss='mse', optimizer='sgd')
    nn_hist = nn_model.fit(X, y, epochs=20, batch_size=5)

    # -----------------------------------------------------------------
    # Visualize neural network training history
    #vis = input('Show neural net training history [y/n]? ')
    vis='n'
    if vis == 'y' or vis == 'yes':
        pd.DataFrame(nn_hist.history).plot(figsize=(12,8))
        plt.grid(True)
        plt.gca().set_ylim(0,1) # set y axis range [0,1]
        plt.show()

    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    joblib.dump(mlp_regressor,os.path.join(models_path, 'mlp_regressor.sav'))
    nn_model.save(os.path.join(models_path, 'nn_model.h5'))

    print('NN models exported successfully.')

if __name__ == '__main__':
    train_nn()