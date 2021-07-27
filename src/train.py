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
    X = train_vals[:,:-1]
    y = train_vals[:,-1]

    ## Support vector regression, polynomial kernel based on the shape of the data
    svr_model = svm.SVR(kernel='poly', degree=2)
    svr_model.fit(X, y)

    # -----------------------------------------------------------------
    # export models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')
    joblib.dump(svr_model, os.path.join(models_path, 'svr_model.pkl'))

    print('SVR models exported successfully.')

if __name__ == '__main__':
    train()
