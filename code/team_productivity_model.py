
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import statsmodels.api as sm
import pandas as pd
from pandas import DataFrame

all_projects = pd.read_csv('../dataset/pullreq_ci/all_projects.csv')
team_productivity = pd.read_csv('../dataset/pullreq_ci/team_productivity.csv')
project_quality = pd.read_csv('../dataset/pullreq_ci/project_quality.csv')

team_productivity_df = DataFrame(team_productivity, columns=['proj_id', 'ci_age', 'n_pr_open', 
    'n_pr_core', 'n_pr_merged', 'n_pr_unmerged', 'n_core_merged', 'n_core_unmerged', 
    'team_size', 'test_files', 'test_loc', 'src_files', 'src_loc', 'n_star', 'n_fork'])

project_quality_df = DataFrame(project_quality, columns=['proj_id', 'ci_age', 'n_bug_issues', 'n_core_bugs'])

all_projects_df = DataFrame(all_projects, columns=['proj_id', 'n_pr'])


print("team productivity, project id, unique values: ", 
        team_productivity_df['proj_id'].nunique())
print("project_quality, project id, unique values: ",
        project_quality_df['proj_id'].nunique())

id_team_productivity = team_productivity_df.set_index(['proj_id']).index
id_project_quality   =   project_quality_df.set_index(['proj_id']).index

res = id_team_productivity.isin(id_project_quality)
res2 = id_project_quality.isin(id_team_productivity)

print("tp which is in pq")
print(len(res))
print("pd which is in tp")
print(len(res2))

team_productivity_new_df = team_productivity_df[res]
project_quality_new_df   = project_quality_df  [res2]

print(team_productivity_new_df)
print(project_quality_new_df)

print("new team productivity, project id, unique values: ", 
        team_productivity_new_df['proj_id'].nunique())
print("new project quality, project id, unique values: ",
        project_quality_new_df['proj_id'].nunique())


counter = 0
for index, row in team_productivity_new_df.iterrows():
    found = False
    for index2, row2 in project_quality_new_df.iterrows():
        if row['proj_id'] == row2['proj_id'] and row['ci_age'] == row2['ci_age']:
            found = True
            break
    if not found:
        print(row['proj_id'], ' and ', row['ci_age'], ' not found')
        project_quality_new_df = project_quality_new_df.append(
                {'proj_id': row['proj_id'], 
                 'ci_age' : row['ci_age'], 
                 'n_bug_issues': 0, 
                 'n_core_bugs': 0}, ignore_index=True)
        counter = counter + 1
        print("found:")
        for index2, row2 in project_quality_new_df.iterrows():
            if row['proj_id'] == row2['proj_id']:
                print(row2['ci_age'], end=',')
        print()

for index2, row2 in project_quality_new_df.iterrows():
    if row['ci_age'] < -12 or row['ci_age'] > 12:
        print("strange: ", row['ci_age'])

print(counter, " not found")

print(team_productivity_new_df)
print(project_quality_new_df)

print("new team productivity, project id, unique values: ", 
        team_productivity_new_df['proj_id'].nunique())
print("new project quality, project id, unique values: ",
        project_quality_new_df['proj_id'].nunique())

print("new team productivity, ci age, unique values: ", 
        team_productivity_new_df['ci_age'].nunique())

print("new project quality, ci age , unique values: ",
        project_quality_new_df['ci_age'].nunique())

print(project_quality_new_df['ci_age'].unique())

id1 = project_quality_new_df[project_quality_new_df['ci_age'] > 12].index
id2 = project_quality_new_df[project_quality_new_df['ci_age'] < -12].index

project_quality_new_df.drop(id1, inplace=True)
project_quality_new_df.drop(id2, inplace=True)

id1 = team_productivity_new_df[team_productivity_new_df['ci_age'] > 12].index
id2 = team_productivity_new_df[team_productivity_new_df['ci_age'] < -12].index

team_productivity_new_df.drop(id1, inplace=True)
team_productivity_new_df.drop(id2, inplace=True)

print("new team productivity, ci age, unique values: ", 
        team_productivity_new_df['ci_age'].nunique())

print("new project quality, ci age , unique values: ",
        project_quality_new_df['ci_age'].nunique())

print(project_quality_new_df['ci_age'].unique())

print(project_quality_new_df)
print(team_productivity_new_df)

merged_df = pd.merge(team_productivity_new_df, 
                    project_quality_new_df, on=['proj_id', 'ci_age'])

print("merged")
print(merged_df)


print("merged unique counter: ", merged_df['proj_id'].nunique())




