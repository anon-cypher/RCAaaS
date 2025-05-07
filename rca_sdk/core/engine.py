
from rca_sdk.utils.plugin_loader import load_plugin
from rca_sdk.llm.generator import generate_summary
from rca_sdk.notifier.dispatcher import dispatch

def run_rca(payload, config):
    service = payload.get("service")
    timestamp = payload.get("timestamp")

    logs_plugin = load_plugin(config["logs"]["module"])
    # ci_plugin = load_plugin(config["ci"]["module"])
    # metrics_plugin = load_plugin(config["metrics"]["module"])

    logs = logs_plugin.get_logs(timestamp, config["logs"])
    # deployments = ci_plugin.get_deployments(service, timestamp)
    # metrics = metrics_plugin.get_metrics(service, timestamp)

    prompt = f"""Analyze the issue using the following data:

Logs:
{logs}

"""

    summary = generate_summary(logs, config)
    dispatch(summary, config["notifications"])
