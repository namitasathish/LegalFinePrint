import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from tasks import analyze_document

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(f.filename)
    upload_dir = app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    path = os.path.join(upload_dir, filename)
    f.save(path)

    task = analyze_document.delay(path)
    return jsonify({"task_id": task.id}), 202

@app.route("/status/<task_id>")
def status(task_id):
    from celery.result import AsyncResult
    res = AsyncResult(task_id, app=analyze_document.app)

    if res.status == "SUCCESS":
        output = res.result
        if isinstance(output, dict):
            if output.get("error") == "NOT_LEGAL":
                return jsonify({"status": "ERROR", "message": "Not a legal document"}), 200
            if output.get("error") == "HF_API_ERROR":
                return jsonify({"status": "ERROR", "message": f"HuggingFace API Error: {output.get('message')}"}), 200
            if output.get("error") == "PROCESSING_FAILED":
                return jsonify({"status": "ERROR", "message": output.get("message")}), 200
            if "results" in output:
                return jsonify({"status": "SUCCESS", "data": output["results"]}), 200

        return jsonify({"status": "ERROR", "message": "Unexpected response format."}), 500

    return jsonify({"status": res.status}), 200

if __name__ == "__main__":
    app.run(debug=True)
