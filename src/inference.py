#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
import joblib
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras

from ga import GeneticAlgorithm

def infer():

    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X = test_vals[:,:-1]
    y = test_vals[:,-1]

    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # load and score models
    svr_path = os.path.join(models_path, 'svr_model.pkl')
    SVR = joblib.load(svr_path)
    SVR_score = SVR.score(X, y)

    mlp_path = os.path.join(models_path, 'mlp_regressor.pkl')
    MLP = joblib.load(mlp_path)
    MLP_score = MLP.score(X, y)

    nn_path = os.path.join(models_path, 'nn_model.h5')
    nn = keras.models.load_model(nn_path)
    nn_score = nn.evaluate(X,y)
    
    # Load scaler models for predictions
    X_scale_path = os.path.join(models_path, 'scalers/X_scale.pkl')
    y_scale_path = os.path.join(models_path, 'scalers/y_scale.pkl')
    X_scale = joblib.load(X_scale_path)
    y_scale = joblib.load(y_scale_path)

    print("--------------------\nInference & Scoring\n--------------------")
    print('=== % Scoring % ===')
    print('SVR Score:', SVR_score)
    print('MLP Score:', MLP_score)
    print('NN MSE Loss:', nn_score)

    # Use genetic algorithm for prediciton and optimization of parameters
    parameters = ['LaserPowerHatch', 'LaserSpeedHatch']
    boundaries = [(100,400), (600,1200)]
    ga_svr = GeneticAlgorithm(SVR, X_scale, y_scale, parameters, boundaries, pop_size=30, mode='minimize')
    ga_mlp = GeneticAlgorithm(MLP, X_scale, y_scale, parameters, boundaries, mode='minimize')
    ga_nn  = GeneticAlgorithm(nn, X_scale, y_scale, parameters, boundaries, mode='minimize')

    # Predict porosity given feature set
    print('\n=== % Predictions % ===')
    data_point = {'LaserPowerHatch':385, 'LaserSpeedHatch':1540}
    svr_porosity = ga_svr.model_predict(data_point)
    mlp_porosity = ga_mlp.model_predict(data_point)
    ga_porosity = ga_nn.model_predict(data_point)
    print(f'Predict {data_point}')
    print(f'SVR Porosity >>> {round(svr_porosity, 4)}')
    print(f'MLP Porosity >>> {round(mlp_porosity, 4)}')
    print(f'ANN Porosity >>> {round(ga_porosity, 4)}')
    
    # Output optimal parameters
    print('\n=== % Optimal Features % ===')
    optimal_features = ga_svr.run(generations=500)
    ga_svr.export(optimal_features)


if __name__ == '__main__':
    infer()