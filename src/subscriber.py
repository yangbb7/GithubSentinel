# 订阅管理模块
class Subscriber:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, repo_url):
        self.subscriptions.append(repo_url)

    def remove_subscription(self, repo_url):
        self.subscriptions.remove(repo_url)

    # 其他订阅管理功能...
