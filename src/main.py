import cmd
import threading
import time
from update_fetcher import UpdateFetcher
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from llm_module import LLMModule


class GitHubSentinel(cmd.Cmd):
    intro = "Welcome to GitHub Sentinel. Type help or ? to list commands.\n"
    prompt = "(Sentinel) "
    file = None

    def __init__(self):
        super().__init__()
        self.subscription_manager = SubscriptionManager()
        self.update_fetcher = UpdateFetcher()
        self.report_generator = ReportGenerator(LLMModule())
        self.scheduler_running = False

    def do_add(self, repo_url):
        "Add a repository to subscriptions: add user/repo"
        self.subscription_manager.add_subscription(repo_url)
        print(f"Added subscription: {repo_url}")

    def do_remove(self, repo_url):
        "Remove a repository from subscriptions: remove user/repo"
        self.subscription_manager.remove_subscription(repo_url)
        print(f"Removed subscription: {repo_url}")

    def do_list(self, _):
        "List all subscriptions"
        subscriptions = self.subscription_manager.list_subscriptions()
        for sub in subscriptions:
            print(sub)

    def do_fetch(self, _):
        "Fetch updates for all subscriptions"
        for repo in self.subscription_manager.list_subscriptions():
            issues, prs = self.update_fetcher.fetch_issues_and_prs(repo)
            self.update_fetcher.export_to_markdown(repo, issues, prs)
            print(f"Exported daily progress for {repo}")

    def do_search(self, keyword):
        "Search for high-star projects by keyword: search <keyword>"
        projects = self.update_fetcher.fetch_top_projects_by_keyword(keyword)
        if isinstance(projects, list):
            for project in projects:
                print(f"{project['full_name']}: {project['stargazers_count']} stars")
        else:
            print(projects['error'])

    def do_generate_report(self, _):
        "Generate summarized report from Markdown files"
        self.report_generator.generate_daily_report()
        print("Generated daily report")

    def do_start_scheduler(self, _):
        "Start the background scheduler"
        if not self.scheduler_running:
            self.scheduler_running = True
            threading.Thread(target=self.scheduler).start()
            print("Scheduler started.")
        else:
            print("Scheduler is already running.")

    def do_stop_scheduler(self, _):
        "Stop the background scheduler"
        self.scheduler_running = False
        print("Scheduler stopped.")

    def scheduler(self):
        while self.scheduler_running:
            self.do_fetch(None)
            time.sleep(86400)  # Run daily

    def do_exit(self, _):
        "Exit the tool"
        print("Exiting GitHub Sentinel.")
        return True


if __name__ == "__main__":
    GitHubSentinel().cmdloop()