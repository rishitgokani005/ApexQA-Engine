import os
import sys
import json
import requests
from utils.config import Config

def send_slack_notification(status: str, total: int, passed: int, failed: int, skipped: int, duration: float):
    """
    Sends a rich Slack Block Kit notification payload via incoming webhook.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL", Config.SLACK_WEBHOOK_URL)
    
    if not webhook_url:
        print("[INFO] SLACK_WEBHOOK_URL not configured. Skipping Slack notification.")
        return

    report_url = os.getenv("ALLURE_REPORT_URL", Config.ALLURE_REPORT_URL)
    github_ref = os.getenv("GITHUB_REF_NAME", "local-run")
    github_actor = os.getenv("GITHUB_ACTOR", "Local Runner")
    commit_sha = os.getenv("GITHUB_SHA", "HEAD")[:7]

    is_success = (failed == 0) and (status.upper() != "FAILURE")
    color = "#36a64f" if is_success else "#e01e5a"
    title_emoji = "✅" if is_success else "🚨"
    header_text = f"{title_emoji} ApexQA-Engine Test Execution Summary ({status.upper()})"

    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": header_text,
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Branch:* `{github_ref}`"},
                            {"type": "mrkdwn", "text": f"*Triggered By:* `{github_actor}`"},
                            {"type": "mrkdwn", "text": f"*Commit:* `{commit_sha}`"},
                            {"type": "mrkdwn", "text": f"*Duration:* `{duration}s`"}
                        ]
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Total Tests:* {total}"},
                            {"type": "mrkdwn", "text": f"*Passed:* ✅ `{passed}`"},
                            {"type": "mrkdwn", "text": f"*Failed:* ❌ `{failed}`"},
                            {"type": "mrkdwn", "text": f"*Skipped:* ⚠️ `{skipped}`"}
                        ]
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "📊 View Allure Live Report",
                                    "emoji": True
                                },
                                "url": report_url,
                                "style": "primary" if is_success else "danger"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            print("[INFO] Slack notification delivered successfully.")
        else:
            print(f"[WARNING] Slack webhook returned status code: {response.status_code}, response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to send Slack notification: {e}")

if __name__ == "__main__":
    # Command line usage: python utils/slack_notifier.py <status> <total> <passed> <failed> <skipped> <duration>
    if len(sys.argv) >= 7:
        status_arg = sys.argv[1]
        total_arg = int(sys.argv[2])
        passed_arg = int(sys.argv[3])
        failed_arg = int(sys.argv[4])
        skipped_arg = int(sys.argv[5])
        duration_arg = float(sys.argv[6])
        send_slack_notification(status_arg, total_arg, passed_arg, failed_arg, skipped_arg, duration_arg)
    else:
        print("Usage: python slack_notifier.py <status> <total> <passed> <failed> <skipped> <duration>")
