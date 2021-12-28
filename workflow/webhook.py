import requests
import json


def webhook(action: str, data: dict):
    webhook_url = f"http://104.131.14.144/workflow/webhook?action={action}"
    payload = {
        "data": data
    }
    r = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={
            "Content-type": "application/json"
        }
    )
