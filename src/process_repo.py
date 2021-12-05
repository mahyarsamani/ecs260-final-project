import os
import argparse

from excavator.developer import Developer
from excavator.excavate import get_repo, get_issues, get_pulls, get_commits

def process_issues(repo, devs, start_index, num_requests_already_made = 0):
    index = start_index
    issues, num_requests_already_made = get_issues(repo,
        num_requests_already_made=num_requests_already_made)

    for issue in issues:
        opener_login = issue.user.login
        if opener_login in devs:
            devs[opener_login].add_issue_opened()
        else:
            dev = Developer(index)
            dev.add_issue_opened()
            devs[opener_login] = dev
            index += 1

        if issue.state == "closed":
            closer_login = issue.closed_by.login
            if closer_login in devs:
                devs[closer_login].add_issue_closed()
            else:
                dev = Developer(index)
                dev.add_issue_closed()
                devs[closer_login] = dev
                index += 1

    return devs, index, num_requests_already_made

def process_prs(repo, devs, start_index, num_requests_already_made = 0):
    index = start_index
    pulls, num_requests_already_made = get_pulls(repo,
        num_requests_already_made=num_requests_already_made)

    for pull in pulls:
        opener_login = pull.user.login

        if opener_login:
            if opener_login in devs:
                devs[opener_login].add_pr_opened()
            else:
                dev = Developer(index)
                dev.add_pr_opened()
                devs[opener_login] = dev
                index += 1

        if pull.merged:
            merger_login = pull.merged_by.login
            if merger_login in devs:
                devs[merger_login].add_pr_merged()
            else:
                dev = Developer(index)
                dev.add_pr_merged()
                devs[merger_login] = dev
                index += 1

        if pull.state == "closed" and not pull.merged:
            closer_login = pull.user.login
            if closer_login in devs:
                devs[closer_login].add_issue_closed()
            else:
                dev = Developer(index)
                dev.add_pr_closed()
                devs[closer_login] = dev
                index += 1

    return devs, index, num_requests_already_made

def process_commits(repo, devs, start_index):
    index = start_index
    commits = get_commits(repo)
    for commit in commits:
        if commit:
            if commit.author:
                if commit.author.login:
                    try:
                        author_login = commit.author.login
                        if author_login in devs:
                            devs[author_login].add_commit()
                        else:
                            dev = Developer(index)
                            dev.add_commit()
                            devs[author_login] = dev
                            index += 1
                    except Exception as e:
                        print(f"{__name__}: {e}")

    return devs, index

def dump_to_csv(devs, out_file):
    out_file.write("developer,issue_opened,issue_closed,pr_opened,pr_closed,pr_merged,commits\n")
    for _, dev in devs.items():
        out_file.write(f"{dev}\n")

def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("gh_token", type=str)
    parser.add_argument("repo_name", type=str)
    parser.add_argument("out_name", type=str)
    args = parser.parse_args()
    outfile_name = os.path.join("../dataset", args.out_name)
    return args.gh_token, args.repo_name, outfile_name

if __name__ == "__main__":
    token, repo_name, outfile = get_inputs()

    repo = get_repo(repo_name, token)

    devs = {}
    start_id = 0
    requests = 0

    devs, new_start_id, requests = process_issues(repo, devs, start_id, num_requests_already_made=requests)
    devs, new_start_id, requests = process_prs(repo, devs, new_start_id, num_requests_already_made=requests)
    devs, new_start_id = process_commits(repo, devs, new_start_id)

    print(f"Made {requests} requests and created {new_start_id} devs.")
    with open(outfile, "w") as outfile:
        dump_to_csv(devs, outfile)
