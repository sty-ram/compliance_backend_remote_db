
from flask import Flask
from flask_cors import CORS

from controllers.auth_controller import auth
from controllers.mapping_controller import mapping
from controllers.image_controller import images
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

print("APP INSTANCE:", id(app))

# GLOBAL CORS FIX – Applies to all routes
CORS(app, supports_credentials=True)

# Register blueprints AFTER app + CORS initialized
app.register_blueprint(auth)
app.register_blueprint(mapping)
app.register_blueprint(images)

# --- HEALTH ENDPOINT ---
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200
if __name__ == "__main__":
    @app.after_request

    def debug_cors(response):

        print("CORS HEADER:", response.headers.get("Access-Control-Allow-Origin"))
        return response

    app.run(host="0.0.0.0", port=6100, debug=True)
    
