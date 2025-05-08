
import importlib

def load_plugin(module_path):
    module = importlib.import_module(module_path)
    return module
