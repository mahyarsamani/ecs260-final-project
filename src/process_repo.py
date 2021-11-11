import os

from github import Github

class Developer():
    def __init__(self, dev_id):
        self.id = dev_id
        self.num_issues_closed = 0
        self.num_pr_opened = 0
        self.num_pr_closed = 0
        self.num_pr_merged = 0
        self.num_commits = 0

    def add_issue_closed(self, inc = 1):
        self.num_issues_closed += inc

    def add_pr_opened(self, inc = 1):
        self.num_pr_opened += inc

    def add_pr_closed(self, inc = 1):
        self.num_pr_closed += inc

    def add_pr_merged(self, inc = 1):
        self.num_pr_merged += inc

    def add_commit(self, inc = 1):
        self.num_commits += inc

    def __str__(self):
        return f"{self.id},{self.num_issues_closed},{self.num_pr_opened},{self.num_pr_closed},{self.num_pr_merged},{self.num_commits}"

    def __repr__(self):
        return str(self)

def get_repo(repo):
    token = os.getenv("GITHUB_TOKEN", "...")
    git = Github(token)
    return git.get_repo(repo)

def get_issues(repo, state):
    return repo.get_issues(state=state)

def get_pull_requests(repo, pr_state):
    return repo.get_pulls(state=pr_state)

def process_issues(repo, devs, start_index):
    index = start_index
    issues = get_issues(repo, "closed")

    for issue in issues:
        if issue.closed_by is None:
            continue
        if issue.closed_by.login is None:
            continue

        developer_login = issue.closed_by.login

        if developer_login in devs:
            devs[developer_login].add_issue_closed()
        else:
            dev = Developer(index)
            dev.add_issue_closed()
            devs[developer_login] = dev
            index += 1

    return devs, index

def process_prs(repo, devs, start_index):
    index = start_index
    prs = get_pull_requests(repo, "closed")

    for pr in prs:
        opener_login = pr.user.login
        if opener_login in devs:
            devs[opener_login].add_pr_opened()
        else:
            dev = Developer(index)
            dev.add_pr_opened()
            devs[opener_login] = dev
            index += 1

        if pr.merged:
            merger_login = pr.merged_by.login
            if merger_login in devs:
                devs[merger_login].add_pr_merged()
            else:
                dev = Developer(index)
                dev.add_pr_merged()
                devs[merger_login] = dev
                index += 1
        elif pr.state == "closed":
            user_login = pr.user.login
            if user_login in devs:
                devs[user_login].add_pr_closed()
            else:
                dev = Developer(index)
                dev.add_pr_closed()
                devs[user_login] = dev
                index += 1

    return devs, index

def process_commits(repo, devs):
    for dev_login in devs.keys():
        devs[dev_login].add_commit(inc=repo.get_commits(author=dev_login).totalCount)
    return devs

def dump_to_csv(devs, out_file):
    out_file.write("Developer,Num_bugs,PR_opened,PR_closed,PR_merged,Num_commits\n")
    for _, dev in devs.items():
        out_file.write(f"{dev}\n")

if __name__ == "__main__":
    repo = get_repo("gunrock/gunrock")

    devs = {}
    start_id = 0

    devs, new_start_id = process_issues(repo, devs, start_id)
    devs, new_start_id = process_prs(repo, devs, new_start_id)
    devs = process_commits(repo, devs)

    with open("../dataset/gunrock.csv", "w") as outfile:
        dump_to_csv(devs, outfile)
