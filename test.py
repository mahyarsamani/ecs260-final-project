from pydriller import Repository

def print_commits(repo, branch):
    for commit in Repository(repo, only_in_branch=branch).traverse_commits():
        print("Hash: {}, Author: {}".format(commit.hash, commit.author.name))

def get_num_pr(repo):
    git_repo = Repository(repo)

print(type(Repository("gem5/")))