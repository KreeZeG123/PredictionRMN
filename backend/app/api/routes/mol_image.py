from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from app.api.services.molecule_image_generator import generate_molecule_image_with_atom_ids

mol_image_bp = Blueprint('mol_image', __name__)

@mol_image_bp.route('/getMolImageWithIds', methods=['POST'])
def get_mol_image_with_ids():
    data = request.get_json()
    smiles = data.get('SMILES')
    if not smiles:
        return jsonify({"error": "Missing 'SMILES' parameter"}), 400

    try:
        image_bytes_io = generate_molecule_image_with_atom_ids(smiles)

        return send_file(
            image_bytes_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='molecule.png'
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error: " + str(e)}), 500
