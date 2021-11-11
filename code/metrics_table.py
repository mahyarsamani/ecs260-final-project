import pandas as pd  # To read data
import matplotlib.pyplot as plt
from pandas.plotting import table 

# Reference: https://www.learndatasci.com/tutorials/predicting-housing-prices-linear-regression-using-python-pandas-statsmodels/
from IPython.core.display import HTML, display
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.sandbox.regression.predstd import wls_prediction_std

## Load data from csv as dataframe and process data
df_csv = pd.read_csv('../dataset/metrics_dummydata.csv')

num_commits_mean = df_csv["Num_commits"].mean()
num_commits_median = df_csv["Num_commits"].median()

num_bugs_mean = df_csv["Num_bugs"].mean()
num_bugs_median = df_csv["Num_bugs"].median()

PR_opened_mean = df_csv["PR_opened"].mean()
PR_opened_median = df_csv["PR_opened"].median()

PR_closed_mean = df_csv["PR_closed"].mean()
PR_closed_median = df_csv["PR_closed"].median()

PR_merged_mean = df_csv["PR_merged"].mean()
PR_merged_median = df_csv["PR_merged"].median()

PR_unmerged_mean = df_csv["PR_unmerged"].mean()
PR_unmerged_median = df_csv["PR_unmerged"].median()


## Create table
data = {'Metrics':['num_commits','num_bugs','num_PRopened','num_PRclosed','num_PRmerged','num_PRunmerged'],
        'Description':['Total number of commits per repository','Total number of bugs and/or issues after each project release',
                        'Total number of opened pull requests per repository','Total number of closed pull requests per repository',
                        'Total number of merged pull requests per repository','Total number of unmerged pull requests per repository'],
        'Mean':[num_commits_mean, num_bugs_mean, PR_opened_mean, PR_closed_mean, PR_merged_mean, PR_unmerged_mean],
        'Median':[num_commits_median, num_commits_median, PR_opened_median, PR_closed_median, PR_merged_median, PR_unmerged_median]}

df = pd.DataFrame(data)

print(df)

fig = plt.figure(figsize=(15,10))
ax = plt.subplot(641, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

tb = table(ax, df, loc='left',colWidths=[1, 2.8, 0.4, 0.4])  # where df is your data frame
tb.auto_set_font_size(False)
tb.set_fontsize(14)
tb.scale(1,3)
plt.savefig('../results/metrics_table.png', bbox_inches='tight', pad_inches=0.1)

