import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pandas import DataFrame
import glob
import math

for filename in glob.glob('../dataset/*.csv'):
    
    print('Dataset: ', filename)

    dataset = pd.read_csv(filename)

    data_df = DataFrame(dataset, columns=['developer', 'issue_opened', 'issue_closed', 
                'pr_opened', 'pr_closed', 'pr_merged', 'commits'])

    print('Size: ', end='')
    print(data_df.shape)

    for index,row in data_df.iterrows():
        for x in row:
            if math.isnan(x):
                print("There is nan: ", row)

    
    print("The number of unique developers: ", end='')
    print(data_df['developer'].nunique(), end='. ')
   
    print()
    
    print("Total number of commits: ", end='')
    print(data_df['commits'].sum())
    
    ### Predicators (explanatory variables):
    ## issues_opened
    ## issues_closed
    ## pr_opened
    ## pr_closed
    ## pr_merged
    
    ### Outcome response variable:
    ## commits
    
    data_mean = data_df['commits'].mean()
    data_var = data_df['commits'].var()
   
    if data_var > data_mean:
        print('Is outcome varaible over-dispersed? (the variance much larger than the mean?)')
        print("The mean of the number of commits: ", end='')
        print(data_mean, end='. ')
    
        print("The variance of the number of commits: ", end='')
        print(data_var)
  
    #np.seterr('raise')

    

    predictors = []
    formula = "commits ~ "
    first = True

    pr_c_zeroes_num    = (data_df['pr_closed'] == 0).sum()
    pr_c_nonzeroes_num = (data_df['pr_closed'] != 0).sum()
    
    print("pr_closed, nonzeroes = ", pr_c_nonzeroes_num, ", zeroes: ", pr_c_zeroes_num)

    if pr_c_nonzeroes_num != 0:
        predictors.append('pr_closed')
        formula = formula + "pr_closed "
        first = False

    pr_o_zeroes_num    = (data_df['pr_opened'] == 0).sum()
    pr_o_nonzeroes_num = (data_df['pr_opened'] != 0).sum()
    
    print("pr_opened, nonzeroes = ", pr_o_nonzeroes_num, ", zeroes: ", pr_o_zeroes_num)

    if pr_o_nonzeroes_num != 0:
        predictors.append('pr_opened')
        if not first:
            formula = formula + " + "
        else:
            first = False
        formula = formula + "pr_opened"

    pr_m_zeroes_num    = (data_df['pr_merged'] == 0).sum()
    pr_m_nonzeroes_num = (data_df['pr_merged'] != 0).sum()
    
    print("pr_opened, nonzeroes = ", pr_m_nonzeroes_num, ", zeroes: ", pr_m_zeroes_num)

    if pr_m_nonzeroes_num != 0:
        predictors.append('pr_merged')
        if not first:
            formula = formula + " + "
        else:
            first = False
        formula = formula + "pr_merged"

    i_o_zeroes_num    = (data_df['issue_opened'] == 0).sum()
    i_o_nonzeroes_num = (data_df['issue_opened'] != 0).sum()
    
    print("issue_opened, nonzeroes = ", i_o_nonzeroes_num, ", zeroes: ", i_o_zeroes_num)

    if i_o_nonzeroes_num != 0:
        predictors.append('issue_opened')
        if not first:
            formula = formula + " + "
        else:
            first = False
        formula = formula + "issue_opened"

    i_c_zeroes_num    = (data_df['issue_closed'] == 0).sum()
    i_c_nonzeroes_num = (data_df['issue_closed'] != 0).sum()
    
    print("issue_closed, nonzeroes = ", i_c_nonzeroes_num, ", zeroes: ", i_c_zeroes_num)

    if i_c_nonzeroes_num != 0:
        predictors.append('issue_closed')
        if not first:
            formula = formula + " + "
        else:
            first = False
        formula = formula + "issue_closed"

    print("predictors:", predictors)
    print("formula: ", formula)

    y = data_df['commits']
    X = data_df[predictors]

    from statsmodels.stats.outliers_influence import variance_inflation_factor
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    vif["features"] = X.columns
    vif.round(1)
    print(vif)

    zeroes_num    = (data_df['commits'] == 0).sum()
    nonzeroes_num = (data_df['commits'] != 0).sum()

    if zeroes_num > nonzeroes_num:
        print('Do the response variables present an excess number of zerose?')

        print("The number of zeroes in commits: ", zeroes_num, end='')
        print("The number of non-zero commits: ", nonzeroes_num, end='')
    
        model = smf.glm(formula = formula, 
                    data=data_df, family=sm.families.NegativeBinomial()).fit()
        print(model.summary())
    print()
    print()
    print()

