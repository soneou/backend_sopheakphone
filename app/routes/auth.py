from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    admin_username = current_app.config["ADMIN_USERNAME"]
    admin_password_hash = current_app.config["ADMIN_PASSWORD_HASH"]

    if not admin_password_hash:
        return jsonify({"error": "Admin account is not configured on the server."}), 500

    if username != admin_username or not check_password_hash(admin_password_hash, password):
        return jsonify({"error": "Invalid username or password."}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token, "username": username})
