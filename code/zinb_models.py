import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.discrete.count_model as smdc
from pandas import DataFrame
import glob
import math
from patsy import dmatrices

data_df = DataFrame(None)

for filename in glob.glob('../dataset/*.csv'):
  
    # does not work
    if filename == '../dataset/latex3.csv' or \
            filename == '../dataset/facebook-react.csv' or \
            filename == '../dataset/pytorch.csv' or \
            filename == '../dataset/electron.csv' or \
            filename == '../dataset/flot.csv' or \
            filename == '../dataset/angularjs.csv' or\
            filename == '../dataset/django.csv' or\
            filename == '../dataset/scikit-learn.csv' or\
            filename == '../dataset/atom.csv' or\
            filename == '../dataset/googleresearch.csv' or\
            filename == '../dataset/googletest.csv' or\
            filename == '../dataset/apple.csv' or\
            filename == '../dataset/numpy.csv' or\
            filename == '../dataset/nvidia-docker.csv' or\
            filename == '../dataset/duckduckgo.csv' or\
            filename == '../dataset/matplotlib.csv' or\
            filename == '../dataset/vscode.csv' or\
            filename == '../dataset/keras.csv' or\
            filename == '../dataset/bitcoin.csv' or\
            filename == '../dataset/tensorflow.csv' or\
            filename == '../dataset/ethereum.csv' or\
            filename == '../dataset/ethereum-org-website.csv' or\
            filename == '../dataset/facebook-react-native.csv':
        continue

    # work!
    #if filename == '../dataset/unity.csv' or\
    #        filename == '../dataset/cisco-mindmeld.csv':
    #    continue

    print('Dataset: ', filename)

    dataset = pd.read_csv(filename)

    data_df0 = DataFrame(dataset, columns=['developer', 'issue_opened', 'issue_closed', 
                'pr_opened', 'pr_closed', 'pr_merged', 'commits'])

    data_df0['team_size'] = data_df0.shape[0]

    data_df = pd.concat([data_df, data_df0])

    formula = "commits ~ issue_opened + pr_opened + pr_merged + team_size"

    y, X = dmatrices(formula, data_df, return_type='dataframe')

    inflated = data_df[['commits', 'pr_opened', 'pr_merged', 'issue_opened']]

    #model = smdc.ZeroInflatedNegativeBinomialP(endog=y, exog=X).fit()
    model = smdc.ZeroInflatedNegativeBinomialP(endog=y, exog=X, exog_infl=inflated, inflation='logit').fit()

    print(model.summary())

    data_stat = DataFrame(None)
    data_stat['Statistics'] = ['Mean', 'St. Dev.', 'min', 'median', 'max']
    data_stat['commits'] =   [data_df['commits'].mean(), 
                              data_df['commits'].std(),
                              data_df['commits'].min(),
                              data_df['commits'].median(),
                              data_df['commits'].max()]
    data_stat['pr_opened'] = [data_df['pr_opened'].mean(), 
                              data_df['pr_opened'].std(),
                              data_df['pr_opened'].min(),
                              data_df['pr_opened'].median(),
                              data_df['pr_opened'].max()]
    data_stat['pr_merged'] = [data_df['pr_merged'].mean(), 
                              data_df['pr_merged'].std(),
                              data_df['pr_merged'].min(),
                              data_df['pr_merged'].median(),
                              data_df['pr_merged'].max()]
    data_stat['issue_opened'] = [data_df['issue_opened'].mean(), 
                                 data_df['issue_opened'].std(),
                                 data_df['issue_opened'].min(),
                                 data_df['issue_opened'].median(),
                                 data_df['issue_opened'].max()]

    print(data_stat)

    print()
    print()
    print()
