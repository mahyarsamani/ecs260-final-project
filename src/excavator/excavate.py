from time import sleep
from github import Github, Repository
from pydriller import Repository as DrillerRepo

def get_repo(repo_name, token):
    git = Github(token)
    return git.get_repo(repo_name)

def get_issues_and_pulls(repo: Repository, limit):
    issues = []
    pulls = []
    requests = 0
    index = 1

    while True:
        if requests and (requests % limit == 0):
            sleep(3600)
        try:
            item = repo.get_issue(index)
            requests += 1
            if not item.pull_request:
                issues.append(item)
                index += 1
            else:
                item = repo.get_pull(index)
                pulls.append(item)
                index += 1
                requests += 1
        except:
            print(f"Ended at index {index}.")
            break

    return issues, pulls, requests

def get_commits(repo: Repository):
    repo_url = f"https://github.com/{repo.full_name}.git"
    return DrillerRepo(path_to_repo=repo_url).traverse_commits()
