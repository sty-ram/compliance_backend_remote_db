from flask import Blueprint, request, jsonify, session
from models.mappings import MAPPINGS
  # wherever your mapping dictionary lives

mapping = Blueprint("mapping", __name__)

@mapping.route("/get_mappings", methods=["POST"])
def get_mappings():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    country = data.get("country")
    entity = data.get("entity")
    product = data.get("product")

    if not (country and entity and product):
        return jsonify({"error": "Missing fields"}), 400

    try:
        result = MAPPINGS[country][entity][product]
        return jsonify({
            "docs": list(set(result["docs"])),
            "compliance": list(set(result["compliance"]))
        })
    except KeyError:
        return jsonify({"error": "Invalid selection"}), 400
