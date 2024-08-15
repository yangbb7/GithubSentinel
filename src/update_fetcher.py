import requests
import yaml


class UpdateFetcher:
    def __init__(self):
        with open('../config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.token = config['github_token']

    def fetch_latest_release(self, repo_url):
        response = requests.get(
            f"https://api.github.com/repos/{repo_url}/releases/latest",
            headers={"Authorization": f"token {self.token}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not fetch release info for {repo_url}: {response.status_code}"}
