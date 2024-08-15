import unittest
from llm_module import LLMModule


class TestLLMModule(unittest.TestCase):
    def setUp(self):
        self.llm = LLMModule()

    def test_summarize_report(self):
        text = "Test issue and pull request summary."
        summary = self.llm.summarize_report(text)
        self.assertIsInstance(summary, str)
