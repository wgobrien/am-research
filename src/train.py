#!/usr/bin/python3
# train.py
# William O'Brien 07/08/2021

import pandas as pd
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn import svm

def train():

    print("--------------------\nTraining SVR Models\n--------------------")

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
    
    # -----------------------------------------------------------------
    # EnergyDensityCalculated
    X = train_vals[:,-2].reshape(-1,1)
    
    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model2 = svm.SVR(kernel='poly', degree=2)
    svr_model2.fit(X, y)

    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    joblib.dump(svr_model1, os.path.join(models_path, 'svr_model1.pkl'))
    joblib.dump(svr_model2, os.path.join(models_path, 'svr_model2.pkl'))

    print('SVR models exported successfully.')

if __name__ == '__main__':
    train()
