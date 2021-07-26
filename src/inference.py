#!/usr/bin/python3
# inference.py
# William O'Brien 07/08/2021

import pandas as pd
import joblib
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras

from ga import *

def infer():

    # read in test data, split parameters and labels
    test_path = os.path.join(os.path.dirname(__file__), '../data/processed/test.csv')
    test = pd.read_csv(test_path)
    test_vals = test.values
    
    X = test_vals[:,:-2]
    y = test_vals[:,-1]

    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # load and score models
    svr1_path = os.path.join(models_path, 'svr_model1.pkl')
    SVR1 = joblib.load(svr1_path)
    SVR1_score = SVR1.score(X, y)

    mlp_path = os.path.join(models_path, 'mlp_regressor.pkl')
    MLP = joblib.load(mlp_path)
    MLP_score = MLP.score(X, y)

    nn_path = os.path.join(models_path, 'nn_model.h5')
    nn = keras.models.load_model(nn_path)
    nn_score = nn.evaluate(X,y)

    # change parameters to energy density
    X = test_vals[:,-2].reshape(-1,1)
    
    svr2_path = os.path.join(models_path, 'svr_model2.pkl')
    SVR2 = joblib.load(svr2_path)
    SVR2_score = SVR2.score(X, y)
    
    # Load scaler models for predictions
    X_scale_path = os.path.join(models_path, 'scalers/X_scale.pkl')
    y_scale_path = os.path.join(models_path, 'scalers/y_scale.pkl')
    X_scale = joblib.load(X_scale_path)
    y_scale = joblib.load(y_scale_path)

    print("--------------------\nInference & Scoring\n--------------------")
    print('--- % Scoring % ---')
    print('SVR Score:', SVR1_score)
    print('SVR Score Energy Density:', SVR2_score)
    print('MLP Score:', MLP_score)
    print('NN Score:', nn_score)

    # Predict porosity given feature set
    print('\n--- % Predictions % ---')
    features = [300,1200,55]
    svr1_porosity = model_predict(features, SVR1, X_scale, y_scale)
    mlp_porosity = model_predict(features, MLP, X_scale, y_scale)
    print(f'Predict {{{features[0]}}} LaserPowerHatch & {{{features[1]}}} LaserSpeed')
    print(f'SVR Porosity >>> {round(svr1_porosity, 4)}')
    print(f'MLP Porosity >>> {round(mlp_porosity, 4)}')

    svr2_porosity = model_predict(features, SVR2, X_scale, y_scale, energy=True)
    print(f'\nPredict {{{features[2]}}} EnergyDensity')
    print(f'SVR Porosity >>> {round(svr2_porosity,4)}')
    
    print('\n--- % Optimal Features % ---')
    optimal_features = ga_walk(SVR1, X_scale, y_scale)
    print(f'Minimal Porosity @ [LaserPowerHatch={{{optimal_features[0]}}}, LaserSpeedHatch={{{optimal_features[1]}}}]')


def ga_walk(model, X_scale, y_scale):
    '''
    input:
        model - SVR or NN model to run GA over
        X_scale, y_scale - scalers used to transform data, feeds into model_predict()
    output:
        array holding optimal feature set

    Genetic algorithm implementation using the model as a basis for regression,
    will output the feature set that optimizes the model's performance (ie minimizes
    porosity)
    '''
    params = [0, 0]

    

    return params

if __name__ == '__main__':
    infer()