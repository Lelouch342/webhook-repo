from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["webhookdb"]
events_collection = db["events"]


def serialize_event(event):
    """
    Convert MongoDB document into JSON serializable format
    """
    return {
        "id": str(event["_id"]),
        "author": event["author"],
        "action": event["action"],
        "from_branch": event.get("from_branch"),
        "to_branch": event.get("to_branch"),
        "timestamp": event["timestamp"].isoformat()
    }


@app.route("/")
def home():
    return "MongoDB connected successfully!"


@app.route("/events", methods=["GET"])
def get_events():

    events = events_collection.find() \
        .sort("timestamp", -1) \
        .limit(20)

    return jsonify([
        serialize_event(event) for event in events
    ])


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")



def parse_github_timestamp(timestamp_str):
    return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))


@app.route("/webhook", methods=["POST"])
def github_webhook():

    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if not payload or not event_type:
        return jsonify({"error": "Invalid webhook data"}), 400

    event_data = None

    try:

        # -------- PUSH EVENT --------
        if event_type == "push":

            event_data = {
                "request_id": payload["after"],
                "author": payload["pusher"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": payload["ref"].split("/")[-1],
                "timestamp": parse_github_timestamp(
                    payload["head_commit"]["timestamp"]
                )
            }

        # -------- PULL REQUEST + MERGE --------
        elif event_type == "pull_request":

            action = payload["action"]
            pr = payload["pull_request"]

            # PR opened
            if action == "opened":

                event_data = {
                    "request_id": str(pr["id"]),
                    "author": pr["user"]["login"],
                    "action": "PULL_REQUEST",
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "timestamp": parse_github_timestamp(
                        pr["created_at"]
                    )
                }

            # MERGE (bonus)
            elif action == "closed" and pr["merged"]:

                event_data = {
                    "request_id": str(pr["id"]),
                    "author": pr["merged_by"]["login"],
                    "action": "MERGE",
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "timestamp": parse_github_timestamp(
                        pr["merged_at"]
                    )
                }

        if not event_data:
            return jsonify({"message": "Event ignored"}), 200

        # Prevent duplicates
        existing = events_collection.find_one({
            "request_id": event_data["request_id"],
            "action": event_data["action"]
        })

        if existing:
            return jsonify({"message": "Duplicate ignored"}), 200

        events_collection.insert_one(event_data)

        return jsonify({"message": "Event stored"}), 201

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"error": "Processing failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
