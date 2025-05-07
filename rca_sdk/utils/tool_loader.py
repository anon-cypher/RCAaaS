import importlib
import inspect
from langchain.tools import Tool
from rca_sdk.plugins.code.local import get_code_snippet  # always included

def load_registered_tools(config):
    tools = []

    for section, entry in config.items():
        mod_path = entry.get("module")
        if not mod_path:
            continue

        try:
            module = importlib.import_module(mod_path)
        except ImportError as e:
            print(f"[❌ Import Error] Could not import module '{mod_path}': {e}")
            continue

        for name, obj in inspect.getmembers(module):
            if callable(obj):
                if hasattr(obj, "_tool"):
                    try:
                        tools.append(Tool.from_function(obj))
                    except Exception as e:
                        print(f"[❌ Tool Error] Failed to load tool '{name}': {e}")
                else:
                    print(f"[⚠️ Skipping] '{name}' is callable but not a LangChain @tool-decorated function.")

    # Always add internal code tool
    if isinstance(get_code_snippet, Tool):
        tools.append(get_code_snippet)
    else:
        print("[❌] get_code_snippet is not a valid LangChain Tool")
    return tools
