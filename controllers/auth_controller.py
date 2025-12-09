# from flask import Blueprint, request, jsonify, session
# from werkzeug.security import generate_password_hash, check_password_hash
# from services.db_service import create_user, fetch_user

# auth = Blueprint("auth", __name__)
# print("AUTH BLUEPRINT LOADED")

# @auth.route("/signup", methods=["POST"])
# def signup():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Missing credentials"}), 400

#     hashed = generate_password_hash(password)
#     result = create_user(username, hashed)

#     if result.get("status") == "error":
#         return jsonify({"error": "Username exists"}), 400

#     return jsonify({"message": "User created"}), 201

# @auth.route("/signin", methods=["POST"])
# def signin():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     user = fetch_user(username)
#     if user and check_password_hash(user["password"], password):
#         session["user"] = username
#         return jsonify({"message": "Signed in"}), 200

#     return jsonify({"error": "Invalid credentials"}), 401

# @auth.route("/logout", methods=["POST"])
# def logout():
#     session.pop("user", None)
#     return jsonify({"message": "Logged out"}), 200

from flask import Blueprint, request, jsonify, session
from services.db_service import create_user, fetch_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# Signup
@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    hashed = generate_password_hash(password)
    result = create_user(username, hashed)

    if "error" in result:
        return jsonify({"error": result["error"]}), result["code"]

    return jsonify({"message": "User created"}), 201


# Signin
@auth.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = fetch_user(username)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["username"] = username
    return jsonify({"message": "Signed in"}), 200


# Logout
@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200
