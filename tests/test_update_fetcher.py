import unittest
from datetime import datetime

from update_fetcher import UpdateFetcher


class TestUpdateFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = UpdateFetcher()

    def test_fetch_issues_and_prs(self):
        # Assume 'octocat/Hello-World' is a valid repo for testing
        issues, prs = self.fetcher.fetch_issues_and_prs('octocat/Hello-World')
        self.assertIsInstance(issues, list)
        self.assertIsInstance(prs, list)

    def test_export_to_markdown(self):
        issues = [{'title': 'Issue 1', 'html_url': 'http://example.com/issue1'}]
        prs = [{'title': 'PR 1', 'html_url': 'http://example.com/pr1'}]
        self.fetcher.export_to_markdown('octocat/Hello-World', issues, prs)
        # Check if the file is created
        import os
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"daily_reports/octocat_Hello-World_{date_str}.md"
        self.assertTrue(os.path.exists(file_name))
