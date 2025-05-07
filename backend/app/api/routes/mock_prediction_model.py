import importlib
from flask import Blueprint, request, jsonify
import json
import os

mock_bp = Blueprint('mock', __name__)

@mock_bp.route('/mockPredictionModel', methods=['POST'])
def mock_prediction_model():
    data = request.get_json()
    smiles = data.get("smiles")

    if not smiles:
        return jsonify({"error": "Missing 'smiles' in mock prediction"}), 400

    print("Mock Prediction Parameters:")
    for key, value in data.items():
        if key != "smiles":
            print(f"  - {key}: {value}")

    try:
        with importlib.resources.open_text('app.api.services.mock', 'mockSpectrum.json') as f:
            spectre = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to load mock spectrum: {str(e)}"}), 500

    # Mock spectrum data for the corresponding molecules
    return jsonify({
        "smiles": "CCOC1=CC=C(C(C)=O)C=C1",
        "spectrum": spectre
    }), 200
