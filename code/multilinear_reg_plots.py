### References: 
## https://newbedev.com/how-to-make-a-4d-plot-with-matplotlib-using-arbitrary-data
## https://medium.com/swlh/multi-linear-regression-using-python-44bd0d10082d
## ** https://medium.com/@prasadostwal/multi-dimension-plots-in-python-from-2d-to-6d-9a2bf7b8cc74 
## ** https://aegis4048.github.io/mutiple_linear_regression_and_visualization_in_python

## We want a 5d plot: (using old data)
## Y = num_commits
## X = num_bugs, PR_opened, PR_closed, PR_merged

import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression


#Read cars data from csv
data = pd.read_csv("../dataset/nvidia_dl_examples.csv")

# predictors = ['Num_bugs','PR_opened','PR_closed','PR_merged']
# outcome = 'Num_commits'

X = data[['Num_bugs','PR_opened','PR_closed','PR_merged']]
Y = data['Num_commits']
# X = data[predictors].values.reshape(-1, len(predictors))
# Y = data[outcome].values

ols = LinearRegression()
model = ols.fit(X,Y)
print(model.coef_)
print(model.intercept_)
print(model.score(X,Y))

#Set marker properties
markersize = data['PR_opened']
markercolor = data['Num_bugs']

# customdata = np.stack((data['PR_opened'], data['Num_bugs']), axis=-1)
customdata_set = list(data[['PR_opened','Num_bugs']].to_numpy())

#Make Plotly figure
fig1 = go.Scatter3d(x=data['PR_closed'],
                    y=data['PR_merged'],
                    z=data['Num_commits'],
                    marker=dict(size=markersize,
                                color=markercolor,
                                opacity=1,
                                reversescale=True,
                                colorscale='Portland',
                                showscale=True,
                                colorbar=dict(title='Num_bugs')),
                    line=dict (width=0.02),
                    mode='markers',
                    hovertemplate =
                        '<i>PR_closed</i>: %{x}' +
                        '<br><i>PR_merged</i>: %{y}' +
                        '<br><i>PR_opened</i>: %{customdata[0]}' +
                        '<br><i>Num_bugs</i>: %{customdata[1]}' +
                        '<br><i>Num_commits</i>: %{z}<extra></extra>',
                    customdata=customdata_set)
                    # text = ['{}'.format(i) for i in data['PR_opened']])


#Make Plot.ly Layout
mylayout = go.Layout(scene=dict(xaxis=dict( title="PR_closed"),
                                yaxis=dict( title="PR_merged"),
                                zaxis=dict(title="Num_commits")),)

#Plot
fig = go.Figure(data = [fig1], layout = mylayout)
fig.show()

# #Plot and save html
# plotly.offline.plot({"data": [fig1],
#                      "layout": mylayout},
#                      auto_open=True,
#                      filename=("5DPlot.html"))






# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import pandas as pd 
# import numpy as np

# data = pd.read_csv('../dataset/nvidia_dl_examples.csv').values  # load data set

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# num_bugs = data[:,1] # x
# pr_opened = data[:,2] # y
# pr_closed = data[:,3] # c

# num_commits = data[:, 5] # z
# print(num_commits)

# # x = np.random.standard_normal(100)
# # print(x)
# # y = np.random.standard_normal(100)
# # z = np.random.standard_normal(100)
# # c = np.random.standard_normal(100)

# img = ax.scatter(num_bugs, pr_opened, num_commits, c=pr_closed, cmap=plt.hot())
# fig.colorbar(img)
# plt.show()
