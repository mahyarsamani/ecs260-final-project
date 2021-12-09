import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pandas import DataFrame
import glob
import math
from statsmodels.formula.api import ols
from IPython.core.display import HTML, display
import dataframe_image as dfi
from statistics import mean

file_num = 1
all_filenames = []
all_rsquares = []
const_pvals = []
issue_opened_pvals = []
issue_closed_pvals = []
pr_opened_pvals = []
pr_closed_pvals = []
pr_merged_pvals = []

for filename in sorted(glob.glob('../dataset/*.csv')):
    
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
    

    predictors = []
    formula = "commits ~ "
    first = True

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

    id_max = vif["VIF Factor"].idxmax()
    while id_max >= 0 and vif["VIF Factor"][id_max] >= 5:
        print("there is collinearity!")
        to_drop = vif["features"][id_max]
        #to_drop = "issue_closed"
        print("dropping: ", to_drop)
        X = X.drop(columns=[to_drop])
        print("new columns: ", X.columns)
        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
        vif["features"] = X.columns
        vif.round(1)
        print(vif)
        id_max = vif["VIF Factor"].idxmax()

    zeroes_num    = (data_df['commits'] == 0).sum()
    nonzeroes_num = (data_df['commits'] != 0).sum()

    if zeroes_num > nonzeroes_num:
        print('Do the response variables present an excess number of zerose?')

        print("The number of zeroes in commits: ", zeroes_num, end='')
        print("The number of non-zero commits: ", nonzeroes_num, end='')
    
        model = smf.glm(formula = formula, 
                    data=data_df, family=sm.families.NegativeBinomial()).fit()
        print(model.summary())

    ### Multilinear regression summary generation ####
    new_predictors = X.columns.tolist()
    print("new_predictors: ", new_predictors, "\n")
    x_axis = dataset[new_predictors]
    y_axis = dataset['commits']

    sm_x = sm.add_constant(x_axis)

    mlr_model = sm.OLS(y_axis, sm_x).fit()
    print("R-square: \n", mlr_model.rsquared)
    print("P-values: \n", mlr_model.pvalues)

    mlr_model_summary = mlr_model.summary()

    if file_num == 1:
        display(HTML(
        (mlr_model_summary.as_html())))
        with open('../results/mlr.txt', 'w') as fh:
            fh.write(filename)
            fh.write("\n")
            fh.write(mlr_model.summary().as_text())
            fh.write("\n\n")
    else:
        display(HTML(
        (mlr_model_summary.as_html())))
        with open('../results/mlr.txt', 'a') as fh:
            fh.write(filename)
            fh.write("\n")
            fh.write(mlr_model.summary().as_text())
            fh.write("\n\n")

    file_num = file_num + 1

    split1 = filename.rsplit('/', 3)
    split2 = split1[2].rsplit('.')
    all_filenames.append(split2[0])
    all_rsquares.append(round(mlr_model.rsquared, 4))

    pval_const = mlr_model.pvalues.loc['const']
    if ("issue_opened" in new_predictors):
        pval_issue_opened = mlr_model.pvalues.loc['issue_opened']
    else: 
        pval_issue_opened = 'NA'

    if ("issue_closed" in new_predictors):
        pval_issue_closed = mlr_model.pvalues.loc['issue_closed']
    else:
        pval_issue_closed = 'NA'

    if ("pr_opened" in new_predictors):
        pval_pr_opened = mlr_model.pvalues.loc['pr_opened']
    else:
        pval_pr_opened = 'NA'
    
    if ("pr_closed" in new_predictors):
        pval_pr_closed = mlr_model.pvalues.loc['pr_closed']
    else:
        pval_pr_closed = 'NA'

    if ("pr_merged" in new_predictors):
        pval_pr_merged = mlr_model.pvalues.loc['pr_merged']
    else:
        pval_pr_merged = 'NA'

    const_pvals.append(round(pval_const, 6))
    issue_opened_pvals.append(pval_issue_opened)
    issue_closed_pvals.append(pval_issue_closed)
    pr_opened_pvals.append(pval_pr_opened)
    pr_closed_pvals.append(pval_pr_closed)
    pr_merged_pvals.append(pval_pr_merged)

    print()
    print()
    print()
### Create table comparison of r-squares, p-values and average r-squares ###
df = pd.DataFrame({ 'Repositories': all_filenames,
                    'R^2': all_rsquares,
                    'Const p-val': const_pvals,
                    'Issues_opened p-val': issue_opened_pvals,
                    'Issues_closed p-val': issue_closed_pvals,
                    'PR_opened p-val': pr_opened_pvals,
                    'PR_closed p-val': pr_closed_pvals,
                    'PR_merged p-val': pr_merged_pvals})

df = df.style.hide_index()
dfi.export(df, '../results/summary.png')

### Create table of averages ###
avg_rsquares = mean(all_rsquares)
print("avg_rsquares: ", avg_rsquares)
avg_constp = mean(const_pvals)
print("avg_constp: ", avg_constp)

issue_opened_pvals_new = []
issue_closed_pvals_new = []
pr_opened_pvals_new = []
pr_closed_pvals_new = []
pr_merged_pvals_new = []

for val in issue_opened_pvals:
    if(val != 'NA'):
        issue_opened_pvals_new.append(val)
avg_issue_opened_pvals = mean(issue_opened_pvals_new)

for val in issue_closed_pvals:
    if(val != 'NA'):
        issue_closed_pvals_new.append(val)
avg_issue_closed_pvals = mean(issue_closed_pvals_new)

for val in pr_opened_pvals:
    if(val != 'NA'):
        pr_opened_pvals_new.append(val)
avg_pr_opened_pvals = mean(pr_opened_pvals_new)

print(pr_closed_pvals)
if(all(elem == 'NA' for elem in pr_closed_pvals)):
    avg_pr_closed_pvals = 'NA'
else:
    for val in pr_closed_pvals:
        if(val != 'NA'):
            pr_closed_pvals_new.append(val)
    print(pr_closed_pvals_new)
    avg_pr_closed_pvals = mean(pr_closed_pvals_new)
print(avg_pr_closed_pvals)


for val in pr_merged_pvals:
    if(val != 'NA'):
        pr_merged_pvals_new.append(val)
avg_pr_merged_pvals = mean(pr_merged_pvals_new)

df2 = pd.DataFrame({ 'Avg. R^2': [avg_rsquares],
                    'Avg. Const p-val': [avg_constp],
                    'Avg. Issues_opened p-val': [avg_issue_opened_pvals],
                    'Avg. Issues_closed p-val': [avg_issue_closed_pvals],
                    'Avg. PR_opened p-val': [avg_pr_opened_pvals],
                    'Avg. PR_closed p-val': [avg_pr_closed_pvals],
                    'Avg. PR_merged p-val': [avg_pr_merged_pvals]})
                    
df2_transposed = df2.T
dfi.export(df2_transposed, '../results/average_summary.png')
