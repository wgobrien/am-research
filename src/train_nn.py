#!/usr/bin/python3
# train_nn.py
# William O'Brien 07/08/2021

import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow.keras as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from sklearn.neural_network import MLPRegressor

def train_nn():
    print("--------------------\nTraining NN Models\n--------------------")
    fpath = '../data/processed/train.csv' # train.csv file path from src
    f_train = os.path.join(os.path.dirname(__file__), fpath) # objective file path to data
    train = pd.read_csv(f_train) # read in training data
    train_vals = train.values # convert pandas dataframe to numpy matrix

    # -----------------------------------------------------------------
    # LaserPowerHatch, LaserSpeedHatch, HatchSpacing, LaserPowerContour
    X = train_vals[:,:-1]
    y = train_vals[:,-1]

    # ----------------------------------------------------------------- 
    # NN Model Builds

    ## Multi-layer Perceptor ANN 
    mlp_regressor = MLPRegressor(hidden_layer_sizes=(5,), alpha=.08, activation='relu', solver='lbfgs')
    mlp_regressor.fit(X, y)

    ## Functional DNN
    in_layer = layers.Input(shape=X.shape[1:])
    h1 = layers.Dense(5, activation='relu')(in_layer)
    h2 = layers.Dense(5, activation='relu')(h1)
    concat = layers.Concatenate()([in_layer, h2])
    out = layers.Dense(1, activation='linear')(concat)
    nn_model = models.Model(inputs=[in_layer], outputs=[out])

    ## Sequential DNN
    nn_model = models.Sequential([
        layers.Dense(5, input_shape=X.shape[1:]
                    , activation='relu'
                    , kernel_regularizer=tf.regularizers.L1(0.08)
                    , activity_regularizer=tf.regularizers.L2(0.08)),
        layers.Dense(1)
    ])

    nn_model.compile(loss='mse', optimizer='sgd')
    nn_hist = nn_model.fit(X, y, epochs=50, verbose=0)
    print(nn_model.summary())

    # -----------------------------------------------------------------
    # Visualize neural network training history
    visual = input('Show neural net training history [y/n]? ')
    if visual == 'y' or visual == 'yes':
        pd.DataFrame(nn_hist.history).plot(figsize=(12,8))
        plt.grid(True)
        plt.gca().set_ylim(0,1) # set y axis range [0,1]
        plt.show()

    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    joblib.dump(mlp_regressor,os.path.join(models_path, 'mlp_regressor.pkl'))
    nn_model.save(os.path.join(models_path, 'nn_model.h5'))

    print('NN models exported successfully.')


    print('\nQuick scoring')
    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X_test = test_vals[:,:-1]
    y_test = test_vals[:,-1]


    print('mlp_score:', mlp_regressor.score(X_test,y_test))
    print('dnn_score:', nn_model.evaluate(X_test, y_test, verbose=0))

if __name__ == '__main__':
    train_nn()
