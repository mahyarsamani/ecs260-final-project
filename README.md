# SPACE Project

## Installation

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

## Intro

In order for us to create a model for productivity we need to gather the following
information for each aspect of SPACE.

* Performance: Number of bugs (number of issues)
* Activity: Number of pull requests (open and close)
* Communication: Number of pull requests

As a baseline we will use the number of commits to measure productivity:

* We can easily get this with pydriller.

The page limit for the progress report.

## Plan

We aim to develop a linear model to predict productivity. This model has five
preditctors (at this stage). These predictors are listed as follows:

* Number of bugs reported
* Number of pull requests opened per month
* Number of pull requests closed per month
* Number of merged pull requests
* Number of unmerged pull requests

These predictors will predict an outcome which is the number of commits.

## Division of labor:

* Agnieszka and Mahyar will be responsible for extracting information.
1. Agnieszka will gather information about pull requests
2. Mahyar will gather information about issues (bugs).
3. Deliverables: python module that does these

* Alicia and Veronica will work on developing a model:
1. Developing a linear model using data analysis modules in python
2. Create dummy data for your model and develop that model
3. Deliverable: Jupyter Notebook to create model and plot graphs

## Note

Never push your code to master branch, rather create a branch with your name (just a suggestion) and then create a PR.

## Datasets

For each project we gather the follwoing data:
* _developer\_id_
* _time_window_
* _issue_opened_
* _issue_closed_
* _pr_opened_
* _pr_closed_
* _pr_merged_
* _commits_

## Plots list

1. Statistics for the selected GitHub projects. (Language, issues, PRs, commits)
2. Statistics on the metrics related to productivity over a period of 12 time windows: mean, st. dev, min, median, max
   for: _issue_opened_, _issue_closed_, _pr_opened_, _pr_closed_, _pr_merged_, _commits_.
3. Results
