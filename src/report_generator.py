class ReportGenerator:
    def __init__(self):
        pass

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
