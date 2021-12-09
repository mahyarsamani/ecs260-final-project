import pandas as pd  # To read data
import matplotlib.pyplot as plt
from pandas.plotting import table

# Reference: https://www.learndatasci.com/tutorials/predicting-housing-prices-linear-regression-using-python-pandas-statsmodels/
from IPython.core.display import HTML, display
import statsmodels.api as sm
from statsmodels.formula.api import ols
import glob
import dataframe_image as dfi
from statistics import mean

filenum = 1
all_filenames = []
all_rsquares = []
const_pvals = []
issue_opened_pvals = []
for filename in sorted(glob.glob('../dataset/*.csv')):
    df_csv = pd.read_csv(filename)

    x1 = df_csv['issue_opened']
    y1 = df_csv['commits']
    x1 = sm.add_constant(x1)
    productivity_performance_model = sm.OLS(y1, x1).fit()
    print(productivity_performance_model.params) # prints [intercept, regression coefficient]
    if (productivity_performance_model.params[1] == 0): # if regression coefficient = 0, skip dataset
        continue
    else:
        productivity_performance_model_summary = productivity_performance_model.summary()
        display(HTML(
        (productivity_performance_model_summary.as_html())))
        if filenum == 1:
            with open('../results/prod_perfopen.txt', 'w') as fh:
                fh.write(filename)
                fh.write("\n")
                fh.write(productivity_performance_model.summary().as_text())
                fh.write("\n")
        else: 
            with open('../results/prod_perfopen.txt', 'a') as fh:
                fh.write(filename)
                fh.write("\n")
                fh.write(productivity_performance_model.summary().as_text())
                fh.write("\n")

    filenum = filenum + 1

    split1 = filename.rsplit('/', 3)
    split2 = split1[2].rsplit('.')
    all_filenames.append(split2[0])

    all_rsquares.append(round(productivity_performance_model.rsquared, 4))

    pval_const = productivity_performance_model.pvalues.loc['const']
    pval_issue_opened = productivity_performance_model.pvalues.loc['issue_opened']

    const_pvals.append(round(pval_const, 6))
    issue_opened_pvals.append(pval_issue_opened)

    print()
    print()
    print()

### Create table comparison of r-squares, p-values and average r-squares ###
df = pd.DataFrame({ 'Repositories': all_filenames,
                    'R^2': all_rsquares,
                    'Const p-val': const_pvals,
                    'Issues_opened p-val': issue_opened_pvals})

df = df.style.hide_index()
dfi.export(df, '../results/issue_opened_summary.png')

### Create table of averages ###
avg_rsquares = mean(all_rsquares)
print("avg_rsquares: ", avg_rsquares)

avg_constp = mean(const_pvals)
print("avg_constp: ", avg_constp)

issue_opened_pvals_new = []
for val in issue_opened_pvals:
    if(val != 'NA'):
        issue_opened_pvals_new.append(val)
avg_issue_opened_pvals = mean(issue_opened_pvals_new)


df2 = pd.DataFrame({ 'Avg. R^2': [avg_rsquares],
                    'Avg. Const p-val': [avg_constp],
                    'Avg. Issues_opened p-val': [avg_issue_opened_pvals]})

df2_transposed = df2.T
dfi.export(df2_transposed, '../results/issue_opened_avgs.png')