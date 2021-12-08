import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pandas import DataFrame
import glob
import math



data_df = DataFrame(None)

for filename in glob.glob('../dataset/*.csv'):
    
    print('Dataset: ', filename)

    dataset = pd.read_csv(filename)

    data_df0 = DataFrame(dataset, columns=['developer', 'issue_opened', 'issue_closed', 
                'pr_opened', 'pr_closed', 'pr_merged', 'commits'])

    print("the number of developers: ", data_df0.shape[0])

    data_df0['team_size'] = data_df0.shape[0]

    data_df = pd.concat([data_df, data_df0])

    print(data_df.shape)

    formula = "commits ~ team_size + issue_opened + pr_opened + pr_merged"
    
    print(data_df)
    
    model = smf.glm(formula = formula, data=data_df, 
                    family = sm.families.NegativeBinomial()).fit()
    
    print(model.summary())
    
    print()
    print()
    print()
