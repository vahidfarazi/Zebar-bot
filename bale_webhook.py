"""
bale_webhook.py

Webhook server for Bale messenger integration.
Receives updates and routes them into Azarakhsh system.
"""

from flask import Flask, request, jsonify

from main_runner import process_update
from logger import log_system, log_error
from main import initialize_system

app = Flask(__name__)


# -----------------------------
# Init system on startup
# -----------------------------
initialize_system()
log_system("bale_webhook", "startup", "Webhook server started")


# -----------------------------
# Webhook endpoint
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Receive updates from Bale bot API.
    """

    try:
        data = request.get_json()

        # -----------------------------
        # Extract basic fields (MVP assumption)
        # -----------------------------
        chat_id = data.get("chat_id")
        message = data.get("message", "")
        role = data.get("role", "USER")

        if not chat_id:
            return jsonify({"ok": False, "error": "missing chat_id"}), 400

        # -----------------------------
        # Process message
        # -----------------------------
        response = process_update(chat_id, message, role)

        # -----------------------------
        # In real Bale integration:
        # here we would send response back via HTTP API
        # -----------------------------

        return jsonify({
            "ok": True,
            "response": response
        })

    except Exception as e:
        log_error("bale_webhook", "webhook_error", str(e))
        return jsonify({
            "ok": False,
            "error": "internal error"
        }), 500


# -----------------------------
# Health check endpoint
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
