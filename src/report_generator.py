import glob
import os
import threading
from pathlib import Path


class ReportGenerator:
    def __init__(self, llm_module):
        self.llm_module = llm_module

    def generate_daily_report(self):
        input_dir = "daily_reports"
        output_dir = "summarized_reports"
        os.makedirs(output_dir, exist_ok=True)

        md_files = glob.glob(f"{input_dir}/*.md")
        threads = [threading.Thread(target=self.process_file, args=(md_file, output_dir)) for md_file in md_files]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def process_file(self, md_file: str, output_dir: str):
        # 使用Pathlib确保路径的安全性
        output_path = Path(output_dir)

        try:
            # 使用'rt'模式确保跨平台兼容性
            with open(md_file, 'rt', encoding='utf-8') as file:
                content = file.read()
                summary = self.llm_module.summarize_report(content)

                # 使用Pathlib处理文件名，增加安全性
                report_name = (output_path / Path(md_file).name.replace(".md", "_daily_report.md"))

                # 使用'wt'模式确保跨平台兼容性
                with open(report_name, 'wt', encoding='utf-8') as report_file:
                    report_file.write(f"# Daily Summary\n\n{summary}")

        except IOError as e:
            print(f"An error occurred while processing the file: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
