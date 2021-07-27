#!/usr/bin/python3
# vis.py
# William O'Brien 07/14/2021

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.preprocessing import MinMaxScaler
import os

def visualize():
    
    path = os.path.join(os.path.dirname(__file__), '../data/interim/interim_data.csv')
    param_data = pd.read_csv(path)

    # export all the figures onto a single pdf
    visuals = PdfPages(os.path.join(os.path.dirname(__file__), '../report/figures/porosity.pdf'))

    # Energy Density vs Porosity
    fig1 = plt.figure(figsize=(12,8))
    plt.loglog(param_data.EnergyDensityCalculated, param_data.Porosity, 'o')
    plt.grid()
    plt.title('Porosity Dependent on Energy Density')
    plt.ylabel('Porosity')
    plt.xlabel('Energy Density')
    visuals.savefig(fig1)
    plt.show()
    
    # parallel coordinates plot
    ## make column for instance labeling, separate by high and low porosities at 50th percentile
    param_data['level']  = pd.qcut(param_data.Porosity, q=[0, 0.5, 1.0], labels =['low porosity','high porosity'])
    ## features to include in the plot
    cols = ['LaserPowerHatch', 'LaserSpeedHatch', 'EnergyDensityCalculated', 'Porosity']
    fig2 = plt.figure(figsize=(12,8))
    plt.title('Relationships between features and outcomes')
    param_data.Porosity = MinMaxScaler(feature_range=(0,1200)).fit_transform(param_data.Porosity.values.reshape(-1,1))
    pd.plotting.parallel_coordinates(param_data, class_column='level', cols=cols, color=('#556270', '#4ECDC4'))
    visuals.savefig(fig2)
    plt.show()

    # scatter matrix for correlations and histograms
    pd.plotting.scatter_matrix(param_data[cols], figsize=(12,8))
    plt.suptitle('Correlations Between Features & Distributions')
    visuals.savefig()
    plt.show()

    # close output pdf file
    visuals.close()

    print('figures saved in report/figures as a pdf')

if __name__ == '__main__':
    visualize()