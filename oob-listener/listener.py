"""
STARK INDUSTRIES SQL — OOB Callback Listener
Internal service running on oob-listener:8888 inside the Docker network.
Captures out-of-band HTTP requests triggered by database or challenge interactions.
"""
import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

captured_events = []


@app.route("/callback", methods=["GET", "POST"])
def callback():
    data = request.args.to_dict()
    data.update(request.form.to_dict())
    if request.is_json and request.json:
        data.update(request.json)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": request.remote_addr,
        "headers": dict(request.headers),
        "data": data,
    }
    captured_events.append(event)
    print(f"[OOB LISTENER] Event received: {event}")
    return jsonify({"status": "captured", "event_count": len(captured_events)})


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify({"events": captured_events})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "oob-listener"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
