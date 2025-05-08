import os
import yaml

def load_config(path="config.yaml"):
    """
    Loads the configuration from a YAML file.

    Args:
        path (str): Path to the config file. Default is "config.yaml".

    Returns:
        dict: Parsed configuration as a dictionary.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    with open(path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML config: {e}")
    
    return config
