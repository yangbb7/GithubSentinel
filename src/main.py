from config import Config
from logger import setup_logger
from subscriber import Subscriber
from updater import fetch_updates
from notifier import send_notification
from reporter import generate_report

def main():
    logger = setup_logger()
    subscriber = Subscriber()
    # 配置订阅
    subscriber.add_subscription('owner/repo1')
    subscriber.add_subscription('owner/repo2')

    # 获取更新
    updates = fetch_updates(subscriber.subscriptions)

    # 发送通知
    send_notification('Updates available!')

    # 生成报告
    report_data = updates  # 假设updates是报告数据
    generate_report(report_data)


if __name__ == "__main__":
    main()
