from openai import OpenAI
import yaml


class LLMModule:
    def __init__(self):
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.api_key = config['openai_api_key']
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    def summarize_report(self, text):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Summarize the following issues and pull requests in Chinese"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
