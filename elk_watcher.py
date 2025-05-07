import time
from datetime import datetime, timedelta
from rca_sdk.utils.config_loader import load_config
from rca_sdk.core.engine import run_rca
from rca_sdk.plugins.logs import elk  # or use plugin loader

config = load_config("config.yaml")

POLL_INTERVAL = 5  # seconds
LOOKBACK_MINUTES = 60
LAST_ALERTED = set()  # avoid duplicate alerts

def is_error(log, keywords):
    message = log.get("message", "")
    return any(k in message for k in keywords)

def poll_elk():
    now = datetime.utcnow()
    since = (now - timedelta(minutes=LOOKBACK_MINUTES)).isoformat()
    keywords = config["logs"]["elasticsearch"].get("error_keywords", [])

    print(f"[🕐] Querying for logs around: {since}")
    logs = elk.get_logs("2025-05-05T13:51:26.301Z", config["logs"])    #2025-05-05T23:10:20.301Z
    # print(logs)

    for log in logs:
        if not isinstance(log, dict):
            print(f"[⚠️  Skipped non-dict log]: {log}")
            continue

        msg = log.get("message", "")
        ts = log.get("@timestamp", "")

        key = f"{ts}:{msg}"

        if key in LAST_ALERTED:
            continue

        if is_error(log, keywords):
            print("[⚠️  Error found]:", msg.strip())
            LAST_ALERTED.add(key)
            payload = {
                "service": "unknown",
                "timestamp": ts
            }
            run_rca(payload, config)


if __name__ == "__main__":
    print("[🔍 ELK watcher started]")
    while True:
        try:
            poll_elk()
        except Exception as e:
            print("[❌ ELK poll failed]:", e)
        time.sleep(POLL_INTERVAL)
