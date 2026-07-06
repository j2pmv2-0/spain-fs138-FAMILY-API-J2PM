"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": "Miembro no encontrado"}), 404
    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data:
        return jsonify({"message": "Solicitud inválida"}), 400

    required_fields = ["first_name", "age", "lucky_numbers"]
    if not all(field in member_data for field in required_fields):
        return jsonify({"message": "Faltan datos requeridos del miembro"}), 400

    new_member = {
        "first_name": member_data.get("first_name"),
        "age": member_data.get("age"),
        "lucky_numbers": member_data.get("lucky_numbers"),
        "id": member_data.get("id")
    }

    member = jackson_family.add_member(new_member)
    return jsonify(member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        return jsonify({"message": "Miembro no encontrado"}), 404
    return jsonify({"done": True}), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
