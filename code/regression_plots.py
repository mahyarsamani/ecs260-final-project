import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
### Reference: https://towardsdatascience.com/linear-regression-in-6-lines-of-python-5e1d0cd05b8d
### Sklearn LinearRegression() finds the best value for the intercept and slope to get the best line of fit.

# read_file = pd.read_excel(r'~\ecs260-final-project\metrics_dummydata.xlsx', sheet_name='metrics_dummydata')
# read_file.to_csv(r'~\ecs260-final-project\metrics_dummydata.csv', index=None, header=True)

data = pd.read_csv('../dataset/scikit-learn.csv')  # load data set

fig, ax = plt.subplots(3, 2, figsize = (8,8)) # 3 rows, 2 columns
fig.suptitle("Scikit-Learn Regression Plots")

num_commits = data.iloc[:, 6].values.reshape(-1, 1)  # (Y-value) values converts it into a numpy array

# ## Performance(num_bugs) vs Productivity(num_commits)
# num_bugs = data.iloc[:, 1].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
# linear_regressor = LinearRegression()  # create object for the class
# linear_regressor.fit(num_bugs, num_commits)  # perform linear regression
# print('Intercept: \n', linear_regressor.intercept_)
# num_commits_pred = linear_regressor.predict(num_bugs)  # make predictions


# ax[0,0].scatter(num_bugs, num_commits)
# ax[0,0].plot(num_bugs, num_commits_pred, color='red')
# ax[0,0].set_title("Performance v.s. Productivity")
# ax[0,0].set_xlabel("Performance(Bugs)")
# ax[0,0].set_ylabel("Productivity(Commits)")


## Performance(issue_opened) vs Productivity(num_commits)
issue_opened = data.iloc[:, 1].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(issue_opened, num_commits)  # perform linear regression
print('Intercept: \n', linear_regressor.intercept_)
num_commits_pred = linear_regressor.predict(issue_opened)  # make predictions


ax[0,0].scatter(issue_opened, num_commits, s=5)
ax[0,0].plot(issue_opened, num_commits_pred, color='red')
ax[0,0].set_title("Performance v.s. Productivity")
ax[0,0].set_xlabel("Performance(Issues opened)")
ax[0,0].set_ylabel("Productivity(Commits)")

## Performance(issue_closed) vs Productivity(num_commits)
issue_closed = data.iloc[:, 2].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(issue_closed, num_commits)  # perform linear regression
print('Intercept: \n', linear_regressor.intercept_)
num_commits_pred = linear_regressor.predict(issue_closed)  # make predictions


ax[0,1].scatter(issue_closed, num_commits, s=5)
ax[0,1].plot(issue_closed, num_commits_pred, color='red')
ax[0,1].set_title("Performance v.s. Productivity")
ax[0,1].set_xlabel("Performance(Issues closed)")
ax[0,1].set_ylabel("Productivity(Commits)")



## Activity(PR_opened) vs Productivity(num_commits)
PR_opened = data.iloc[:, 3].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_opened, num_commits)  # perform linear regression
print('Intercept: \n', linear_regressor.intercept_)
num_commits_pred = linear_regressor.predict(PR_opened)  # make predictions

ax[1,0].scatter(PR_opened, num_commits, s=5)
ax[1,0].plot(PR_opened, num_commits_pred, color='red')
ax[1,0].set_title("Activity v.s. Productivity")
ax[1,0].set_xlabel("Activity(Opened pull requests)")
ax[1,0].set_ylabel("Productivity(Commits)")



## Activity(PR_closed) vs Productivity(num_commits)
PR_closed = data.iloc[:, 4].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_closed, num_commits)  # perform linear regression
print('Intercept: \n', linear_regressor.intercept_)
num_commits_pred = linear_regressor.predict(PR_closed)  # make predictions

ax[1,1].scatter(PR_closed, num_commits, s=5)
ax[1,1].plot(PR_closed, num_commits_pred, color='red')
ax[1,1].set_title("Activity v.s. Productivity")
ax[1,1].set_xlabel("Activity(Closed pull requests)")
ax[1,1].set_ylabel("Productivity(Commits)")


## Communication(PR_merged) vs Productivity(num_commits)
PR_merged = data.iloc[:, 5].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_merged, num_commits)  # perform linear regression
print('Intercept: \n', linear_regressor.intercept_)
num_commits_pred = linear_regressor.predict(PR_merged)  # make predictions

ax[2,0].scatter(PR_merged, num_commits, s=5)
ax[2,0].plot(PR_merged, num_commits_pred, color='red')
ax[2,0].set_title("Communication v.s. Productivity")
ax[2,0].set_xlabel("Communication(Merged pull requests)")
ax[2,0].set_ylabel("Productivity(Commits)")



fig.tight_layout()
plt.savefig('../results/plots.png')
plt.show()

# ## Communication(PR_unmerged) vs Productivity(num_commits)
# PR_unmerged = data.iloc[:, 6].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
# linear_regressor = LinearRegression()  # create object for the class
# linear_regressor.fit(PR_unmerged, num_commits)  # perform linear regression
# num_commits_pred = linear_regressor.predict(PR_unmerged)  # make predictions

# ax[2,0].scatter(PR_unmerged, num_commits)
# ax[2,0].plot(PR_unmerged, num_commits_pred, color='red')
# ax[2,0].set_title("Communication v.s. Productivity")
# ax[2,0].set_xlabel("Communication(Unmerged pull requests)")
# ax[2,0].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 5)
# plt.scatter(PR_unmerged, num_commits)
# plt.plot(PR_unmerged, num_commits_pred, color='red')

