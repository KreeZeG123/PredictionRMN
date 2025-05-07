from flask import Blueprint, jsonify, request
from app.api.services.default_loader import load_default_json
from app.api.services.settings_handler import load_json_file, check_general_settings_format, check_model_parameters_format
from app.config import Config
import json

settings_bp = Blueprint('settings', __name__)

valid_files = {
        "GeneralSettings": "GeneralSettings.json",
        "ModelParameters": "ModelParameters.json"
    }

@settings_bp.route('/loadSettings/<fileName>', methods=['GET'])
def load_settings(fileName):
    if fileName not in valid_files:
        return jsonify({"error": "Invalid file name. Allowed: GeneralSettings, ModelParameters"}), 400

    data, error = load_json_file(valid_files[fileName])
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data)


@settings_bp.route('/saveSettings/<fileName>', methods=['POST'])
def save_settings(fileName):
    if fileName not in valid_files:
        return jsonify({"error": "Invalid file name. Allowed: GeneralSettings, ModelParameters"}), 400

    try:
        content = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
    
    if fileName == "GeneralSettings":
        if not check_general_settings_format(content):
            return jsonify({"error": "Invalid format for GeneralSettings"}), 400
    elif fileName == "ModelParameters":
        if not check_model_parameters_format(content):
            return jsonify({"error": "Invalid format for ModelParameters"}), 400

    try:
        path = Config.get_settings_file_path(valid_files[fileName])
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)
        return jsonify({"message": f"{valid_files[fileName]} saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save settings: {str(e)}"}), 500

@settings_bp.route('/resetToDefault/<fileName>', methods=['POST'])
def reset_to_default(fileName):
    if fileName not in valid_files:
        return jsonify({"error": "Invalid file name. Allowed: GeneralSettings, ModelParameters"}), 400

    default_filename = valid_files[fileName].replace(".json", "Default.json")
    default_data = load_default_json(default_filename)

    if default_data is None:
        return jsonify({"error": f"No default available for '{fileName}'"}), 500

    if fileName == "GeneralSettings":
        if not check_general_settings_format(default_data):
            return jsonify({"error": "Default GeneralSettings format is invalid"}), 500
    elif fileName == "ModelParameters":
        if not check_model_parameters_format(default_data):
            return jsonify({"error": "Default ModelParameters format is invalid"}), 500

    try:
        path = Config.get_settings_file_path(valid_files[fileName])
        with open(path, 'w') as f:
            json.dump(default_data, f, indent=2)
        return jsonify({"message": f"{valid_files[fileName]} has been reset to default."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to reset settings: {str(e)}"}), 500