# rca_sdk/core/generator.py

from openai import OpenAI
from httpx import Timeout, Limits, Client, HTTPTransport

def build_context(logs: list[dict]) -> str:
    """
    Converts list of logs into formatted string for LLM input.
    """
    lines = []
    for log in logs:
        ts = log.get("@timestamp", "")
        msg = log.get("message", "").strip()
        lines.append(f"[{ts}] {msg}")
    return "\n".join(lines)


def build_prompt(logs):
    formatted_logs = "\n".join(logs)
    return f"""
You are an expert observability and diagnostics assistant.

Analyze the following raw log entries and generate a detailed root cause analysis (RCA) summary with the following structure:

---

1. **🕒 Timestamp of Error**
   - Mention exact time the error occurred

2. **🚨 Error Type & Severity**
   - Extract the level (ERROR, WARNING, etc.) and type (if applicable)

3. **📂 File & Line Number**
   - If available, mention file path and line causing the error

4. **🧠 Root Cause**
   - Briefly describe the most likely root cause of failure based on context

5. **📌 Preceding Events**
   - List the events/messages logged just before the error

6. **📋 Traceback Details**
   - If a stack trace is available, summarize what failed and where

7. **🛠️ Suggested Fixes**
   - Provide specific, technical, and actionable remediations

---

### Logs:
{formatted_logs}
"""



# def generate_summary(logs: list[dict], config: dict) -> str:
#     """
#     Main function to generate RCA summary using OpenAI's GPT model.
#     """
#     # Disable SSL cert check
#     transport = HTTPTransport(verify=False)  # ⛔ not for prod use

#     # client = OpenAI(
#     #     api_key=config["rag"]["openai_api_key"],
#     #     http_client=Client(transport=transport, timeout=Timeout(10.0))
#     # )

#     client = OpenAI(
#         base_url=config["rag"]["api_base"],
#         api_key=config["rag"]["api_key"],
#         http_client=Client(transport=transport, timeout=Timeout(10.0))
#     )


#     # client = OpenAI(api_key=config["rag"]["openai_api_key"])
#     log_context = build_context(logs)
#     prompt = build_prompt(log_context)

#     response = client.chat.completions.create(
#         model=config["rag"]["model"],
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2,
#         max_tokens=600
#     )

#     return response.choices[0].message.content.strip()


#TODO: RAG Implementation

from langchain_openai import ChatOpenAI # type: ignore
from langchain.agents import initialize_agent, AgentType
# from langchain.chat_models import ChatOpenAI
from rca_sdk.utils.tool_loader import load_registered_tools
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_summary(logs: list[dict], config: dict) -> str:
   """
   Main function to generate RCA summary using OpenAI's GPT model.
   """
   from langchain.prompts import PromptTemplate
   # Disable SSL cert check
   transport = HTTPTransport(verify=False)  # ⛔ not for prod use
   timestamp = logs[0]["timestamp"]
   service = logs[0]["message"]

   # client = OpenAI(
   #    base_url=config["rag"]["api_base"],
   #    api_key=config["rag"]["api_key"],
   #    http_client=Client(transport=transport, timeout=Timeout(10.0))
   # )
   llm = ChatOpenAI(
    temperature=0.2,
    model=config["rag"]["model"],
    openai_api_key=config["rag"]["api_key"],
    base_url=config["rag"]["api_base"],
    http_client=Client(transport=transport, timeout=Timeout(10.0))
)

   tools = load_registered_tools(config)

   agent = initialize_agent(
      tools=tools,
      llm=llm,
      agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
      verbose=True
   )

   log_lines = []
   for log in logs:
      ts = log.get("@timestamp") or log.get("timestamp")
      msg = log.get("message", "").strip()
      log_lines.append(f"[{ts}] {msg}")
   formatted_logs = "\n".join(log_lines)

   prompt = PromptTemplate.from_template("""
You are an expert observability and diagnostics assistant for software systems.

Analyze the following logs and generate a Root Cause Analysis (RCA) using this exact structure and strict formatting:

---

### Root Cause Analysis:

1. **🕒 Timestamp of Error**
   - Extract the exact timestamp when the error occurred.

2. **🚨 Error Type & Severity**
   - Identify the error level (e.g., ERROR, WARNING) and type (e.g., AttributeError, DivisionByZero).
   - Be specific and use keywords found in the logs.

3. **📂 File & Line Number**
   - If a file or line number is mentioned or can be inferred, include it here. Otherwise, state 'Not available'.

4. **🧠 Root Cause**
   - Clearly explain why the error occurred, with reasoning.
   - Use observed log patterns and missing handling logic.
   - Example: "'NoneType' object has no attribute 'get'" typically means a dictionary key was missing or returned None unexpectedly.

5. **📌 Preceding Events**
   - List the log messages that came just before the error. If none exist, say so.

6. **📋 Traceback Details**
   - If a traceback is found in the logs, summarize it. Otherwise, write 'No traceback available.'

7. **🛠️ Suggested Fixes**
   - If you can identify a specific file and line, suggest an actionable code fix.
   - Otherwise, explain general preventive measures for this class of error.
   - Be specific and technical.

---

Logs to analyze:
{logs}
""")

   chain = LLMChain(prompt=prompt, llm=llm)
   response = chain.run(logs=formatted_logs)

   return response.strip()
   # return agent.invoke(prompt)


