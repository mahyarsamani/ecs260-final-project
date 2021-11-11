import os

from github import Github

class Developer():
    def __init__(self, dev_id):
        self.id = dev_id
        self.num_issues_closed = 0

    def add_issues_closed(self, inc = 1):
        self.num_issues_closed += inc

    def __str__(self):
        return f"(id={self.id}, closed_issues={self.num_issues_closed})"

    def __repr__(self):
        return str(self)

def get_repo(repo):
    token = os.getenv("GITHUB_TOKEN", "...")
    git = Github(token)
    return git.get_repo(repo)

def get_closed_issues(repo):
    return repo.get_issues(state="closed")

def process_isuess(repo):
    index = 0
    login_to_index = dict()
    developers = list()

    issues = get_closed_issues(repo)

    for issue in issues:
        if issue.closed_by is None:
            continue
        if issue.closed_by.login is None:
            continue

        developer_login = issue.closed_by.login

        if developer_login in login_to_index:
            developers[login_to_index[developer_login]].add_issues_closed()
        else:
            developer = Developer(index)
            developer.add_issues_closed()
            login_to_index[developer_login] = index
            index += 1
            developers.append(developer)

    return developers

if __name__ == "__main__":

    repo = get_repo("gunrock/gunrock")

    devs = process_isuess(repo)
    print(devs)
