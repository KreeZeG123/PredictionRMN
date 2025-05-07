from flask import Blueprint, request, jsonify
from app.api.services.kekule_converter import convert_smiles_to_kekule

convert_bp = Blueprint('convert', __name__)

@convert_bp.route('/convertToKekuleSmiles', methods=['POST'])
def convert_to_kekule_smiles():
    data = request.get_json()
    smiles = data.get('SMILES')
    if not smiles:
        return jsonify({"error": "Missing 'SMILES'"}), 400

    try:
        kekule = convert_smiles_to_kekule(smiles)
        return jsonify({"smiles": smiles, "kekule_smiles": kekule})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
