import json
import os


class SubscriptionManager:
    def __init__(self, filename='subscriptions.json'):
        self.filename = filename
        self.subscriptions = self.load_subscriptions()

    def add_subscription(self, repo_url):
        if repo_url not in self.subscriptions:
            self.subscriptions.append(repo_url)
            self.save_subscriptions()

    def remove_subscription(self, repo_url):
        if repo_url in self.subscriptions:
            self.subscriptions.remove(repo_url)
            self.save_subscriptions()

    def list_subscriptions(self):
        return self.subscriptions

    def load_subscriptions(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_subscriptions(self):
        with open(self.filename, 'w') as file:
            json.dump(self.subscriptions, file)