<div align="center">

# RCA SDK: AI-Powered Root Cause Analysis Framework
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LLM](https://img.shields.io/badge/LLM-OpenAI%20%7C%20OpenRouter-purple.svg?logo=openai)](https://openrouter.ai/)
[![Slack Alerts](https://img.shields.io/badge/Alerts-Slack-4A154B.svg?logo=slack&logoColor=white)](https://slack.com/)
[![Observability](https://img.shields.io/badge/Focus-Observability-blueviolet)]()


```

'########:::'######:::::'###::::::::::::::'######::'########::'##:::'##:
 ##.... ##:'##... ##:::'## ##::::::::::::'##... ##: ##.... ##: ##::'##::
 ##:::: ##: ##:::..:::'##:. ##::::::::::: ##:::..:: ##:::: ##: ##:'##:::
 ########:: ##:::::::'##:::. ##:'#######:. ######:: ##:::: ##: #####::::
 ##.. ##::: ##::::::: #########:........::..... ##: ##:::: ##: ##. ##:::
 ##::. ##:: ##::: ##: ##.... ##::::::::::'##::: ##: ##:::: ##: ##:. ##::
 ##:::. ##:. ######:: ##:::: ##::::::::::. ######:: ########:: ##::. ##:
..:::::..:::......:::..:::::..::::::::::::......:::........:::..::::..::

```
</div>

The **RCA SDK** is a lightweight, pluggable, AI-powered framework that automates root cause analysis of application failures by analyzing real-time system logs. It seamlessly integrates with your ELK stack, leverages LLMs for reasoning (e.g., GPT via OpenAI or OpenRouter), and pushes insightful RCA summaries to Slack — all without requiring any code changes or agents.

> 🛠️ Built for DevOps, SREs, and AI + observability workflows. Open source, modular, and ready for experimentation.



## ✅ Current Capabilities

- 🔄 **Real-time log ingestion** via Logstash + Elasticsearch  
- 🧠 **AI-based RCA generation** using GPT models (fully configurable)  
- 📩 **Slack notifications** using incoming webhooks  
- ⚙️ **Simple YAML-based configuration** to customize behavior  



## 🧪 Roadmap & Future Integrations

- ✅ CI/CD pipeline integration (e.g., GitHub Actions)  
- 📊 Anomaly detection on time-series log patterns  
- 💻 Offline inference using local LLMs (e.g., Mistral, LLaMA 3 via Ollama)  
- 🌐 Multi-source log ingestion and multi-channel alerting  



## 📦 Installation

### Step 1: Prerequisites

- Python 3.8+
- Elasticsearch + Logstash (local or remote)
- Slack webhook URL (optional)
- API key for GPT model provider (e.g., OpenAI or OpenRouter)

### Step 2: Clone and Install

```bash
git clone https://github.com/yourusername/rca_sdk.git
cd rca_sdk
pip install -r requirements.txt
```

### Step 3: Configurations

Update `config.yaml` to suit your environment:

```
logs:
  module: rca_sdk.plugins.logs.elk
  elasticsearch:
    host: "http://localhost:9200"
    index: "rca-logs"
    username: "your_elasticsearch_username"
    password: "your_elasticsearch_password"
    use_ssl: false
    error_keywords: ["ERROR", "Exception", "CRITICAL"]

notifications:
  slack:
    module: rca_sdk.plugins.notifications.slack_notifier
    webhook_url: "https://hooks.slack.com/services/your/webhook/url"

rag:
  model: "openai/gpt-3.5-turbo"
  api_base: "https://openrouter.ai/api/v1"
  api_key: "your_api_key"
  provider: "openrouter"

code:
  module: rca_sdk.plugins.code.local
```

### Step 4: Running the SDK

```
python main.py
```

This will:

1. Ingest logs in real-time from ELK.

2. Detect error events and extract critical tracebacks.

3. Generate structured RCA summaries using a GPT model.

4. Send Slack notifications with insights and suggestions.



## 🧩 Architecture
```
ELK Stack --> RCA SDK (LLM-Powered Inference Engine) --> Slack Alerts
```

Modular plugin-based design:

- logs: ingestion plugins

- rag: LLM-powered analysis engine

- notifications: alerting hooks

- code: optional custom logic

## 👨‍💻 Contributing
Contributions are welcome and appreciated!

1. Fork the repository

2. Create your feature branch (git checkout -b feature/amazing-feature)

3. Commit your changes (git commit -am 'Add amazing feature')

4. Push to the branch (git push origin feature/amazing-feature)

5. Open a pull request 🚀


## 💬 Feedback 
Open to feedback, feature suggestions, and use cases!

[![Email](https://img.shields.io/badge/Email-Send%20Mail-red?logo=gmail)](mailto:shubham.sg53147@gmail.com)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/anon-cypher)

