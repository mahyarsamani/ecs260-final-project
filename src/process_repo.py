import os
import argparse

from excavator.developer import Developer
from excavator.excavate import get_repo, get_issues_and_pulls, get_commits

def process_issues(issues, devs, start_index):
    index = start_index
    exceptions = 0

    for issue in issues:
        try:
            opener_login = issue.user.name.lower().replace(" ", "")
            if opener_login in devs:
                devs[opener_login].add_issue_opened()
            else:
                dev = Developer(index)
                dev.add_issue_opened()
                devs[opener_login] = dev
                index += 1

            if issue.state == "closed":
                closer_login = issue.closed_by.name.lower().replace(" ", "")
                if closer_login in devs:
                    devs[closer_login].add_issue_closed()
                else:
                    dev = Developer(index)
                    dev.add_issue_closed()
                    devs[closer_login] = dev
                    index += 1
        except:
            exceptions += 1

    return devs, index, exceptions

def process_pulls(pulls, devs, start_index):
    index = start_index
    exceptions = 0

    for pull in pulls:
        try:
            opener_login = pull.user.name.lower().replace(" ", "")
            if opener_login:
                if opener_login in devs:
                    devs[opener_login].add_pr_opened()
                else:
                    dev = Developer(index)
                    dev.add_pr_opened()
                    devs[opener_login] = dev
                    index += 1

            if pull.merged:
                merger_login = pull.merged_by.name.lower().replace(" ", "")
                if merger_login in devs:
                    devs[merger_login].add_pr_merged()
                else:
                    dev = Developer(index)
                    dev.add_pr_merged()
                    devs[merger_login] = dev
                    index += 1

            if pull.state == "closed" and not pull.merged:
                closer_login = pull.user.name.lower().replace(" ", "")
                if closer_login in devs:
                    devs[closer_login].add_issue_closed()
                else:
                    dev = Developer(index)
                    dev.add_pr_closed()
                    devs[closer_login] = dev
                    index += 1
        except:
            exceptions += 1

    return devs, index, exceptions

def process_commits(repo, devs, start_index):
    index = start_index
    commits = get_commits(repo)
    exceptions = 0

    for commit in commits:
        try:
            author_login = commit.author.name.lower().replace(" ", "")
            if author_login in devs:
                devs[author_login].add_commit()
            else:
                dev = Developer(index)
                dev.add_commit()
                devs[author_login] = dev
                index += 1
        except:
            exceptions += 1

    return devs, index, exceptions

def dump_to_csv(devs, out_file):
    out_file.write("developer,issue_opened,issue_closed,pr_opened,pr_closed,pr_merged,commits\n")
    for _, dev in devs.items():
        out_file.write(f"{dev}\n")

def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("gh_token", type=str)
    parser.add_argument("repo_name", type=str)
    parser.add_argument("rate_limit", type=int)
    parser.add_argument("out_name", type=str)
    args = parser.parse_args()
    outfile_name = os.path.join("../dataset", args.out_name)
    return args.gh_token, args.repo_name, args.rate_limit, outfile_name

if __name__ == "__main__":
    token, repo_name, limit, outfile = get_inputs()

    repo = get_repo(repo_name, token)
    issues, pulls, requests = get_issues_and_pulls(repo, limit)
    devs = {}
    start_id = 0

    devs, start_id, e0 = process_issues(issues, devs, start_id)
    devs, start_id, e1 = process_pulls(pulls, devs, start_id)
    devs, start_id, e2 = process_commits(repo, devs, start_id)

    print(f"Made {requests} requests, created {start_id} devs and ignored {e0}+{e1}+{e2} exceptions.")
    with open(outfile, "w") as outfile:
        dump_to_csv(devs, outfile)
