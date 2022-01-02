import requests
import json
import os


# webhook is sent everytime a product is created or updated
def webhook(action: str, data: dict):
    webhook_url = f"{os.getenv('HOST_URL')}/workflow/webhook?action={action}"
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
