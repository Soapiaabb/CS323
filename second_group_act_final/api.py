import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from supabase import Client, create_client

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def check_vote_data(vote_data):
    # simple lang ni nga validation para sure naa tanan needed fields
    needed_fields = ["user_id", "poll_id", "choice"]

    for field in needed_fields:
        if field not in vote_data or not vote_data[field]:
            return False

    return True


@app.route("/vote", methods=["POST"])
def receive_vote():

    # kuhaon ang gi send nga json sa edge node
    vote_data = request.get_json()

    if not vote_data:
        return jsonify({"error": "No payload received"}), 400

    if not check_vote_data(vote_data):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        queue_data = {
            "user_id": vote_data["user_id"],
            "poll_id": vote_data["poll_id"],
            "choice": vote_data["choice"],
            "timestamp": vote_data.get("timestamp"),
            "node_id": vote_data.get("node_id", "unknown"),
            "status": "pending",
        }

        # diri sa queue una ibutang aron murag pub/sub setup
        supabase.table("vote_queue").insert(queue_data).execute()

        print(
            f"[API] Vote queued from {queue_data['node_id']} -> {queue_data['user_id']}"
        )

        return jsonify({"status": "accepted"}), 200

    except Exception as err:
        print(f"[API] Error while queueing vote: {err}")

        return jsonify({"error": str(err)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("[API] Starting server sa port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
