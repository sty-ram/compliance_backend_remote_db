# #  created for image upload and retrieval

# from flask import Blueprint, request, jsonify, session
# from services.db_service import upload_image_to_db, fetch_user_images

# print("IMAGE BLUEPRINT LOADED")

# images = Blueprint("images", __name__)

# # @images.route("/upload_image", methods=["POST"])
# # def upload_image():
# #     if "user" not in session:
# #         return jsonify({"error": "Unauthorized"}), 401

# #     file = request.files.get("file")
# #     if not file:
# #         return jsonify({"error": "No file"}), 400

# #     username = session["user"]
# #     result = upload_image_to_db(username, file)
# #     return jsonify(result), 200
# @images.route("/upload_image", methods=["POST"])
# def upload_image():
#     if "user" not in session:
#         return jsonify({"error": "Unauthorized"}), 401

#     file = request.files.get("file")
#     doc_type = request.form.get("doc_type")   # NEW

#     if not file:
#         return jsonify({"error": "No file"}), 400

#     if not doc_type:
#         return jsonify({"error": "Missing document type"}), 400

#     username = session["user"]
#     result = upload_image_to_db(username, file, doc_type)
#     return jsonify(result), 200


# # @images.route("/get_images", methods=["GET"])
# # def get_images():
# #     if "user" not in session:
# #         return jsonify({"error": "Unauthorized"}), 401

# #     username = session["user"]
# #     imgs = fetch_user_images(username)
# #     return jsonify(imgs), 200
# # get image to accept optional doc_type filter
# @images.route("/get_images", methods=["GET"])
# def get_images():
#     if "user" not in session:
#         return jsonify({"error": "Unauthorized"}), 401

#     username = session["user"]
#     doc_type = request.args.get("doc_type")  # NEW

#     imgs = fetch_user_images(username, doc_type)
#     return jsonify(imgs), 200


from flask import Blueprint, request, jsonify, session
from services.db_service import upload_image_to_db, fetch_user_images

images = Blueprint("images", __name__)

@images.route("/upload_image", methods=["POST"])
def upload_image():
    # FIX SESSION KEY
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session["username"]
    doc_type = request.form.get("doc_type")
    file = request.files.get("file")

    if not doc_type or not file:
        return jsonify({"error": "Missing doc_type or file"}), 400

    result = upload_image_to_db(username, file, doc_type)
    return jsonify(result), 201


@images.route("/get_images", methods=["GET"])
def get_images():
    # FIX SESSION KEY
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session["username"]
    doc_type = request.args.get("doc_type")

    result = fetch_user_images(username, doc_type)
    return jsonify(result), 200
