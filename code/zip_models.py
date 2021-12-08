import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pandas import DataFrame
import glob
import math
from patsy import dmatrices

data_df = DataFrame(None)

for filename in glob.glob('../dataset/*.csv'):
    
    print('Dataset: ', filename)

    dataset = pd.read_csv(filename)

    data_df0 = DataFrame(dataset, columns=['developer', 'issue_opened', 'issue_closed', 
                'pr_opened', 'pr_closed', 'pr_merged', 'commits'])

    data_df0['team_size'] = data_df0.shape[0]

    data_df = pd.concat([data_df, data_df0])

    formula = "commits ~ issue_opened + pr_opened + pr_merged + team_size"
    #formula = "commits ~ pr_merged + team_size"

    y, X = dmatrices(formula, data_df, return_type='dataframe')
    print(X)

    inflated = data_df[['commits', 'pr_opened', 'pr_merged', 'issue_opened']]

    model = sm.ZeroInflatedPoisson(endog=y, exog=X, exog_infl=inflated, inflation='logit').fit()

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
