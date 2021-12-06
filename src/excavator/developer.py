class Developer():
    def __init__(self, dev_id):
        self.id = dev_id
        self.num_issues_opened = 0
        self.num_issues_closed = 0
        self.num_pr_opened = 0
        self.num_pr_closed = 0
        self.num_pr_merged = 0
        self.num_commits = 0

    def add_issue_opened(self, inc = 1):
        self.num_issues_opened += inc

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
        return f"{self.id},{self.num_issues_opened},{self.num_issues_closed},{self.num_pr_opened},{self.num_pr_closed},{self.num_pr_merged},{self.num_commits}"

    def __repr__(self):
        return str(self)
