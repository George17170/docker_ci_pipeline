import os
import platform
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

START_TIME = datetime.now(timezone.utc)


def uptime_seconds():
    delta = datetime.now(timezone.utc) - START_TIME
    return int(delta.total_seconds())


@app.route("/")
def index():
    return jsonify({
        "service": "docker-ci-pipeline",
        "status": "ok",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "environment": os.getenv("APP_ENV", "local"),
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "uptime_seconds": uptime_seconds(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "host": platform.node(),
    })


@app.route("/pipeline")
def pipeline_info():
    return jsonify({
        "build": {
            "commit_sha": os.getenv("GIT_COMMIT_SHA", "local"),
            "build_number": os.getenv("GITHUB_RUN_NUMBER", "local"),
            "branch": os.getenv("GITHUB_REF_NAME", "local"),
            "built_at": os.getenv("BUILD_TIMESTAMP", "local"),
        },
        "image": {
            "name": "docker-ci-pipeline",
            "version": os.getenv("APP_VERSION", "0.1.0"),
            "registry": os.getenv("DOCKER_REGISTRY", "dockerhub"),
        }
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("APP_ENV", "local") == "local"
    app.run(host="0.0.0.0", port=port, debug=debug)