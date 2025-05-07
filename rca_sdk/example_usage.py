
from rca_sdk.core.engine import run_rca

config = {
    "logs": {"module": "rca_sdk.plugins.logs.elk"},
    "ci": {"module": "rca_sdk.plugins.ci.github_actions"},
    "metrics": {"module": "rca_sdk.plugins.metrics.prometheus"},
    "notifications": {
        "slack": {"webhook_url": "https://hooks.slack.com/services/XXX"},
        "email": {"smtp": "smtp.example.com"}
    }
}

payload = {
    "service": "auth-service",
    "timestamp": "2025-05-03T12:00:00Z"
}

run_rca(payload, config)
