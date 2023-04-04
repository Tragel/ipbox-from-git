import os
import git
import pandas as pd
from datetime import datetime
from loguru import logger
from typing import Dict
import pytz



def find_repos(base_path):
    for root, dirs, _ in os.walk(base_path):
        if ".git" in dirs:
            repo_path = root
            repo_name = os.path.basename(root)
            repo = git.Repo(repo_path)
            logger.info(f"Processing repository {repo_name}")
            yield repo, repo_path
            dirs.remove(".git")

def collect_commit_data(commit, repo_name, branch_name) -> Dict:
    data = {
        "date": commit.committed_datetime,
        "files": commit.stats.files,
        "commit_message": commit.message,
        "repository_name": repo_name,
        "branch_name": branch_name,
    }
    return data


def extract_commits_data(user_email: str, start_date: str, end_date: str, base_path: str) -> pd.DataFrame:
    logger.info("Extracting commit data")

    start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
    end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

    data = []

    for repo, repo_path in find_repos(base_path):
        for branch in repo.branches:
            logger.info(f"Processing {repo=}, {branch.name=}")
            for commit in repo.iter_commits(branch):
                commit_datetime = commit.committed_datetime.replace(tzinfo=pytz.UTC)
                if commit.author.email == user_email and start_date <= commit_datetime <= end_date:
                    commit_data = collect_commit_data(commit, repo_path, branch)
                    data.append(commit_data)


    df = pd.DataFrame(data)
    print(df.head)
    return df











