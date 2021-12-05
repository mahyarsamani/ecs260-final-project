from time import sleep
from github import Github, Repository

def get_repo(repo_name, token):
    git = Github(token)
    return git.get_repo(repo_name)

def get_issues(repo: Repository, num_requests_already_made = 0):
    ret = []
    index = 1
    requests = num_requests_already_made

    try:
        while True:
            if index % 4900 == 0:
                sleep(3600)
            issue = repo.get_issue(index)
            ret.append(issue)
            requests += 1
            index += 1
    except Exception as e:
        print(f"{__name__}: {e}")

    return ret, requests

def get_pulls(repo: Repository, num_requests_already_made = 0):
    ret = []
    index = 1
    requests = num_requests_already_made

    try:
        while True:
            if index % 4900 == 0:
                sleep(3600)
            pull = repo.get_pull(index)
            ret.append(pull)
            requests += 1
            index += 1
    except Exception as e:
        print(f"{__name__}: {e}")

    return ret, requests

def get_commits(repo: Repository):
    return repo.get_commits()
