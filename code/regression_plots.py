import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression

# read_file = pd.read_excel(r'~\ecs260-final-project\metrics_dummydata.xlsx', sheet_name='metrics_dummydata')
# read_file.to_csv(r'~\ecs260-final-project\metrics_dummydata.csv', index=None, header=True)

data = pd.read_csv('../dataset/metrics_dummydata.csv')  # load data set

## Performance(num_bugs) vs Productivity(num_commits)
num_commits = data.iloc[:, 1].values.reshape(-1, 1)  # (Y-value) values converts it into a numpy array

num_bugs = data.iloc[:, 2].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(num_bugs, num_commits)  # perform linear regression
num_commits_pred = linear_regressor.predict(num_bugs)  # make predictions

fig, ax = plt.subplots(3, 2, figsize = (8,8))
ax[0,0].scatter(num_bugs, num_commits)
ax[0,0].plot(num_bugs, num_commits_pred, color='red')
ax[0,0].set_title("Performance v.s. Productivity")
ax[0,0].set_xlabel("Performance(Bugs)")
ax[0,0].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 1)
# plt.scatter(num_bugs, num_commits)
# plt.plot(num_bugs, num_commits_pred, color='red')

## Activity(PR_opened) vs Productivity(num_commits)
PR_opened = data.iloc[:, 3].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_opened, num_commits)  # perform linear regression
num_commits_pred = linear_regressor.predict(PR_opened)  # make predictions

ax[0,1].scatter(PR_opened, num_commits)
ax[0,1].plot(PR_opened, num_commits_pred, color='red')
ax[0,1].set_title("Activity v.s. Productivity")
ax[0,1].set_xlabel("Activity(Opened pull requests)")
ax[0,1].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 2)
# plt.scatter(PR_opened, num_commits)
# plt.plot(PR_opened, num_commits_pred, color='red')


## Activity(PR_closed) vs Productivity(num_commits)
PR_closed = data.iloc[:, 4].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_closed, num_commits)  # perform linear regression
num_commits_pred = linear_regressor.predict(PR_closed)  # make predictions

ax[1,0].scatter(PR_closed, num_commits)
ax[1,0].plot(PR_closed, num_commits_pred, color='red')
ax[1,0].set_title("Activity v.s. Productivity")
ax[1,0].set_xlabel("Activity(Closed pull requests)")
ax[1,0].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 3)
# plt.scatter(PR_closed, num_commits)
# plt.plot(PR_closed, num_commits_pred, color='red')


## Communication(PR_merged) vs Productivity(num_commits)
PR_merged = data.iloc[:, 5].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_merged, num_commits)  # perform linear regression
num_commits_pred = linear_regressor.predict(PR_merged)  # make predictions

ax[1,1].scatter(PR_merged, num_commits)
ax[1,1].plot(PR_merged, num_commits_pred, color='red')
ax[1,1].set_title("Communication v.s. Productivity")
ax[1,1].set_xlabel("Communication(Merged pull requests)")
ax[1,1].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 4)
# plt.scatter(PR_merged, num_commits)
# plt.plot(PR_merged, num_commits_pred, color='red')


## Communication(PR_unmerged) vs Productivity(num_commits)
PR_unmerged = data.iloc[:, 6].values.reshape(-1, 1)  # (X-value) -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(PR_unmerged, num_commits)  # perform linear regression
num_commits_pred = linear_regressor.predict(PR_unmerged)  # make predictions

ax[2,0].scatter(PR_unmerged, num_commits)
ax[2,0].plot(PR_unmerged, num_commits_pred, color='red')
ax[2,0].set_title("Communication v.s. Productivity")
ax[2,0].set_xlabel("Communication(Unmerged pull requests)")
ax[2,0].set_ylabel("Productivity(Commits)")

# plt.subplot(3, 2, 5)
# plt.scatter(PR_unmerged, num_commits)
# plt.plot(PR_unmerged, num_commits_pred, color='red')

fig.tight_layout()
plt.savefig('../results/plots.png')
plt.show()


mlr = LinearRegression()
#mlr.fit(
#        [
#            [getattr(t, 'x%d' % i) for i in range(1, 8)] for t in texts
#            ],
#        [t.y for t in texts])

# Model(ACP) = PR_unmerged + PR_closed + PR_opened + num_bugs, y = num_commits

PR_unmerged = PR_unmerged.reshape(20)
PR_closed = PR_closed.reshape(20)
PR_opened = PR_opened.reshape(20)
num_bugs = num_bugs.reshape(20)
num_commits = num_commits.reshape(20)

print(PR_unmerged.shape)
print(PR_closed.shape)
print(PR_opened.shape)
print(num_bugs.shape)
print(num_commits.shape)

X1 = [x for x in PR_unmerged]
X2 = [x for x in PR_closed]
X3 = [x for x in PR_opened]
X4 = [x for x in num_bugs]

X = [X1, X2, X3, X4]

Y = [x for x in num_commits]

import statsmodels.api as sm
from pandas import DataFrame

Productivity = {'PR_unmerged': X1,
                'PR_closed'  : X2,
                'PR_opened'  : X3,
                'num_bugs'   : X4,
                'num_commits': Y}

print(X4)
print(Y)

df = DataFrame(Productivity, columns=['PR_unmerged', 'PR_closed', 'PR_opened', 'num_bugs', 'num_commits'])

X = df[['PR_unmerged', 'PR_closed', 'PR_opened', 'num_bugs']]
#X = df[['PR_unmerged', 'PR_closed', 'num_bugs']]
#X = df[['PR_closed']]
#X = df['PR_closed']
Y = df['num_commits']

#X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
print_model = model.summary()
print(print_model)

pred_ols = model.get_prediction()
iv_l = pred_ols.summary_frame()["obs_ci_lower"]
iv_u = pred_ols.summary_frame()["obs_ci_upper"]

fig2, ax2 = plt.subplots(figsize=(8, 6))

ax2.plot(X, Y, "o", label="data")
#ax2.plot(X, y_true, "b-", label="True")
ax2.plot(X, model.fittedvalues, "r--.", label="OLS")
ax2.plot(X, iv_u, "r--")
ax2.plot(X, iv_l, "r--")
ax2.legend(loc="best")

plt.savefig('../results/plots2.png')
plt.show()

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    print(X)
    print(y)
    model = sm.OLS(y, X)
    return model

#print(X1)
#print(X2)
#print(X3)
#print(X4)
#print(Y)

#model = reg_m(Y, X)
#results = model.fit()
#print (results.summary())
#print (results.params)
#print (results.tvalues)

##X = np.array([X1, X2, X3, X4]).T
##print("X shape ", X.shape)
##print("y shape ", num_commits.shape)
##
##linear_regressor = LinearRegression()
##reg = linear_regressor.fit(X, num_commits)
##print(reg.score(X, num_commits))
##print(reg.coef_)
##print(reg.intercept_)
##
##productivity = linear_regressor.predict(X)










