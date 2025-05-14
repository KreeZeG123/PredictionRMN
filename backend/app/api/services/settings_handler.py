import os
import json
from app.config import Config
from app.api.services.default_loader import load_default_json
from typing import Any, Tuple

def load_json_file(filename: str) -> Tuple[Any, str]:
    path = Config.get_settings_file_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        default_data = load_default_json(filename.replace(".json", "Default.json"))
        if default_data is None:
            return None, f"No default available for '{filename}'"
        try:
            with open(path, 'w') as f:
                json.dump(default_data, f, indent=4)
            return default_data, None
        except Exception as e:
            return None, f"Failed to create '{filename}': {str(e)}"

    try:
        with open(path, 'r') as f:
            return json.load(f), None
    except Exception as e:
        return None, f"Failed to load '{filename}': {str(e)}"


def check_general_settings_format(data: Any) -> bool:
    if not isinstance(data, list) or not data:
        return False

    for category in data:
        if not isinstance(category, dict):
            return False
        if 'settingsCategoryName' not in category or 'settings' not in category:
            return False
        if not isinstance(category['settings'], list):
            return False

        for setting in category['settings']:
            if not isinstance(setting, dict):
                return False
            required_keys = {'key', 'label', 'type', 'default'}
            if not required_keys.issubset(setting):
                return False
            if setting['type'] not in ['text', 'number', 'select', 'boolean']:
                return False
            if 'options' in setting and not isinstance(setting['options'], list):
                return False
            if 'value' in setting and not isinstance(setting['value'], (str, int, float, bool)):
                return False
    return True


def check_model_parameters_format(data: Any) -> bool:
    if not isinstance(data, dict):
        return False

    if 'currentModel' not in data or 'models' not in data:
        return False

    if not isinstance(data['currentModel'], str):
        return False

    models = data['models']
    if not isinstance(models, list) or not models:
        return False

    for model in models:
        if not isinstance(model, dict):
            return False
        if 'modelName' not in model or 'endpoint' not in model or 'parameters' not in model:
            return False
        if not isinstance(model['modelName'], str) or not isinstance(model['endpoint'], str):
            return False
        if not isinstance(model['parameters'], list):
            return False

        for param in model['parameters']:
            if not isinstance(param, dict):
                return False
            required_keys = {'key', 'label', 'type', 'required'}
            if not required_keys.issubset(param):
                return False
            if param['type'] not in ['text', 'number', 'select', 'boolean']:
                return False
            if not isinstance(param['required'], bool):
                return False
            if 'options' in param and not isinstance(param['options'], list):
                return False
            if 'default' in param and not isinstance(param['default'], (str, int, float, bool)):
                return False
            if 'value' in param and not isinstance(param['value'], (str, int, float, bool)):
                return False

    return True
