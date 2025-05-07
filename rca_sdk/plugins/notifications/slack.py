import requests

def send(message, config):
    webhook_url = config["webhook_url"]
    resp = requests.post(webhook_url, json={"text": message}, verify=False)
    if resp.status_code != 200:
        raise RuntimeError(f"Slack webhook failed: {resp.text}")