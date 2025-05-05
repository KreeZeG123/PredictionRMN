import os
import sys
import json

def get_resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, 'app', 'defaults', relative_path)

def load_default_json(filename):
    path = get_resource_path(filename)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading default json '{filename}': {e}")
        return None
