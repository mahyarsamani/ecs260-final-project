import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pandas import DataFrame
import glob
import math
from patsy import dmatrices

data_df = DataFrame(None)

print(data_df)

for filename in glob.glob('../dataset/*.csv'):
    
    print('Dataset: ', filename)

    dataset = pd.read_csv(filename)

    data_df0 = DataFrame(dataset, columns=['developer', 'issue_opened', 'issue_closed', 
                'pr_opened', 'pr_closed', 'pr_merged', 'commits'])

    data_df0['team_size'] = data_df0.shape[0]

    data_df = pd.concat([data_df, data_df0])

    y = data_df['commits']
    X = data_df[['team_size', 'issue_opened', 'pr_opened', 'pr_merged']]
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    print(model.summary())
    
    print()
    print()
    print()
