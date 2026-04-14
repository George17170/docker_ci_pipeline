# docker-ci-pipeline

A production-grade CI/CD pipeline built with GitHub Actions, Docker, and Python. Demonstrates the full delivery lifecycle — from code push to a tested, versioned Docker image on DockerHub — using the same patterns used in real engineering teams.

![CI/CD Pipeline](https://github.com/George17170/docker-ci-pipeline/actions/workflows/ci.yml/badge.svg)

---

## What this demonstrates

- **Multi-stage Docker builds** — separate builder and runtime stages to keep the final image lean
- **Non-root containers** — application runs as a dedicated `appuser`, not root
- **Docker HEALTHCHECK** — container reports its own health status to Docker and orchestrators
- **3-job GitHub Actions pipeline** — test → build → smoke test, each job gated on the previous
- **DockerHub image publishing** — versioned tags using run number + commit SHA
- **Post-deploy smoke test** — pulls the published image and hits every endpoint to confirm it works
- **Coverage enforcement** — Pytest fails the pipeline if coverage drops below 80%
- **Build metadata injection** — commit SHA, build timestamp, and version baked into the image at build time

---

## Pipeline overview

```
git push to main
       │
       ▼
┌─────────────────┐
│   Job 1: Test   │  Lint (flake8) + Pytest + coverage report
└────────┬────────┘
         │ passes
         ▼
┌─────────────────┐
│  Job 2: Build   │  Docker multi-stage build → push to DockerHub
└────────┬────────┘    tags: latest + 0.1.<run>-<sha>
         │
         ▼
┌─────────────────┐
│ Job 3: Smoke    │  Pull image → run container → hit /health + all endpoints
└─────────────────┘
```

Pull requests only run Job 1 (test + lint). Jobs 2 and 3 only run on pushes to `main`.

---

## Application endpoints

The app is a minimal Flask service that exposes three endpoints. The content of the endpoints is not the point — the infrastructure around them is.

| Endpoint | Description |
|---|---|
| `GET /` | Service name, status, version, environment |
| `GET /health` | Health status, uptime, Python version, hostname |
| `GET /pipeline` | Build metadata: commit SHA, run number, branch, image info |

---

## Project structure

```
docker-ci-pipeline/
├── app/
│   ├── __init__.py
│   └── main.py              # Flask application
├── tests/
│   ├── __init__.py
│   └── test_app.py          # 20 Pytest tests across all endpoints
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions pipeline (3 jobs)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Local development
├── requirements.txt
├── pyproject.toml           # Pytest + coverage config
├── .flake8                  # Lint config
└── .gitignore
```

---

## Running locally

**Without Docker:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest

# Run lint
flake8 app/ tests/

# Start app
python3 -m app.main
# http://localhost:5000
```

**With Docker Compose:**
```bash
docker compose up --build
# http://localhost:5000
```

**Check endpoints:**
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/pipeline
```

---

## Setting up the pipeline on your fork

The pipeline needs two GitHub Secrets to push images to DockerHub:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Add:
   - `DOCKER_USERNAME` — your DockerHub username
   - `DOCKER_TOKEN` — DockerHub access token (generate at hub.docker.com → Account Settings → Security → New Access Token)

The test and lint jobs run without these secrets. Only the build and push job needs them.

---

## Dockerfile design decisions

| Decision | Reason |
|---|---|
| Multi-stage build | Build tools (pip, compilers) stay out of the runtime image — smaller and more secure |
| `python:3.11-slim` | Minimal base image, no unnecessary OS packages |
| Non-root `appuser` | Containers should never run as root in production |
| `HEALTHCHECK` | Docker and Kubernetes use this to decide if a container is ready for traffic |
| `gunicorn` in production | Flask's built-in dev server is not production-safe — gunicorn handles concurrency |
| `PYTHONUNBUFFERED=1` | Ensures logs appear in real time instead of being buffered |

---

## License

CC BY-NC 4.0 — free for personal and educational use, not for commercial use.
See [LICENSE](LICENSE) for full terms.

Author: George Hall — [github.com/George17170](https://github.com/George17170)
