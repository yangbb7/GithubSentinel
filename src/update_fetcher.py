import os
import requests
import yaml
from datetime import datetime


class UpdateFetcher:
    def __init__(self):
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.token = config['github_token']

    def fetch_issues_and_prs(self, repo_url):
        headers = {"Authorization": f"token {self.token}"}
        issues = requests.get(
            f"https://api.github.com/repos/{repo_url}/issues",
            headers=headers
        ).json()

        pull_requests = requests.get(
            f"https://api.github.com/repos/{repo_url}/pulls",
            headers=headers
        ).json()

        return issues, pull_requests

    def export_to_markdown(self, repo_url, issues, pull_requests):
        date_str = datetime.now().strftime("%Y-%m-%d")
        dir_name = "daily_reports"
        os.makedirs(dir_name, exist_ok=True)
        file_name = f"{repo_url.replace('/', '_')}_{date_str}.md"
        file_path = os.path.join(dir_name, file_name)

        with open(file_path, 'w') as file:
            file.write(f"# {repo_url} Daily Report ({date_str})\n\n")
            file.write("## Issues\n")
            for issue in issues:
                file.write(f"- [{issue['title']}]({issue['html_url']})\n")

            file.write("\n## Pull Requests\n")
            for pr in pull_requests:
                file.write(f"- [{pr['title']}]({pr['html_url']})\n")

    def fetch_latest_release(self, repo_url):
        response = requests.get(
            f"https://api.github.com/repos/{repo_url}/releases/latest",
            headers={"Authorization": f"token {self.token}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not fetch release info for {repo_url}: {response.status_code}"}

    def fetch_top_projects_by_keyword(self, keyword):
        query = f"stars:>10000 {keyword} in:name,description"
        response = requests.get(
            f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc",
            headers={"Authorization": f"token {self.token}"}
        )
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            return {"error": f"Failed to fetch projects: {response.status_code}"}