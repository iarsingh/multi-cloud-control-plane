# Multi-cloud control plane

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/controlplane/main.py`](src/controlplane/main.py) | HTTP handlers: `POST /plans` |
| [`src/controlplane/plan.py`](src/controlplane/plan.py) | Functions: `build_plan` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_plan.py`](tests/test_plan.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn controlplane.main:app --reload
```

<!-- project-guide:end -->

Level: Advanced+

Skills: GCP, AWS, Azure, Terraform types, APIs

One request names a cloud, a resource (`bucket` or `cluster`), and a name. The response is a plan with the Terraform type for that cloud. `applied` is false. No credential is read.

```bash
pip install -r requirements.txt
pytest -q
```

