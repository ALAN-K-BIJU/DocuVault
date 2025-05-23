from flask import Blueprint, jsonify

user_bp = Blueprint('users', __name__)

@user_bp.route('/status')
def status():
    return jsonify({"status": "User service active."})