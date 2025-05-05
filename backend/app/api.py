from flask import Blueprint, request, jsonify
from rdkit import Chem
from rdkit.Chem import rdmolops
from .default_loader import load_default_json
import os
import json
from app.config import Config

api_routes = Blueprint('api', __name__)

@api_routes.route('/convertToKekuleSmiles', methods=['POST'])
def convert_to_kekule_smiles():
    data = request.get_json()

    if 'SMILES' not in data:
        return jsonify({"error": "Missing 'SMILES' in the request"}), 400
    
    smiles = data['SMILES']


    mol = Chem.MolFromSmiles(smiles)
    if mol:
        try:
            Chem.Kekulize(mol, clearAromaticFlags=True)
            kekulized = Chem.MolToSmiles(mol, canonical=True, kekuleSmiles=True)
            return jsonify({
                "smiles" : smiles,
                "kekule_smiles": kekulized
            })
        except Exception as e:
            return jsonify({
                "smiles": smiles,
                "error": f"An error occurred: {str(e)}"
            }), 500
            
    else:
        return jsonify({
            "error": f"[{smiles}] SMILES invalide"
        }); 500

def load_json_file(filename):
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
    
@api_routes.route('/loadSettings/<fileName>', methods=['GET'])
def load_settings(fileName):
    valid_files = {
        "GeneralSettings": "GeneralSettings.json",
        "ModelParameters": "ModelParameters.json"
    }

    if fileName not in valid_files:
        return jsonify({"error": "Invalid file name. Allowed: GeneralSettings, ModelParameters"}), 400

    data, error = load_json_file(valid_files[fileName])
    if error:
        return jsonify({"error": error}), 500
    return jsonify(data)

@api_routes.route('/saveSettings/<fileName>', methods=['POST'])
def save_settings(fileName):
    valid_files = {
        "GeneralSettings": "GeneralSettings.json",
        "ModelParameters": "ModelParameters.json"
    }

    if fileName not in valid_files:
        return jsonify({"error": "Invalid file name. Allowed: GeneralSettings, ModelParameters"}), 400

    try:
        content = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

    try:
        path = Config.get_settings_file_path(valid_files[fileName])
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)
        return jsonify({"message": f"{valid_files[fileName]} saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save settings: {str(e)}"}), 500