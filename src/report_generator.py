import glob
from concurrent.futures import ThreadPoolExecutor


class ReportGenerator:
    def __init__(self, llm_module):
        self.llm_module = llm_module

    def generate_daily_report(self):
        md_files = glob.glob("daily_reports/*.md")
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_file, md_files)

    def process_file(self, md_file):
        with open(md_file, 'r') as file:
            content = file.read()
            summary = self.llm_module.summarize_report(content)
            report_name = md_file.replace(".md", "_daily_report.md")
            with open(report_name, 'w') as report_file:
                report_file.write(f"# Daily Summary\n\n{summary}")

    def generate_release_report(self, release_info):
        if "error" in release_info:
            return release_info["error"]
        try:
            report = f"Latest Release Report for {release_info['name']}\n"
            report += f"Tag: {release_info['tag_name']}\n"
            report += f"Published at: {release_info['published_at']}\n"
            report += f"Body: {release_info['body']}\n"
            return report
        except KeyError:
            return "Error: Incomplete release information."
