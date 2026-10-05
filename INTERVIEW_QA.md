# multi-cloud-control-plane — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does multi-cloud-control-plane address, and what can you demonstrate?

One request names a cloud, a resource (`bucket` or `cluster`), and a name. The response is a plan with the Terraform type for that cloud. `applied` is false. No credential is read.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/controlplane/main.py`](src/controlplane/main.py): Implementation or supporting configuration.
- [`src/controlplane/plan.py`](src/controlplane/plan.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_plan.py`](tests/test_plan.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `build_plan` and explain the decision it makes?

The main walkthrough here is `build_plan(cloud, resource, name)` in [`src/controlplane/plan.py`](src/controlplane/plan.py#L8).

```python
def build_plan(cloud, resource, name):
    kind = RESOURCES[cloud][resource]
    return {
        "cloud": cloud,
        "resource": resource,
        "name": name,
        "terraform_type": kind,
        "applied": False,
    }
```

## 4. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(status_code=422, detail='cloud must be gcp, aws, or azure')` in [`src/controlplane/main.py`](src/controlplane/main.py#L18).
- `HTTPException(status_code=422, detail='resource must be bucket or cluster')` in [`src/controlplane/main.py`](src/controlplane/main.py#L20).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_plan.py`](tests/test_plan.py#L8) contains `test_three_clouds_share_a_plan_and_nothing_is_applied`:

```python
def test_three_clouds_share_a_plan_and_nothing_is_applied():
    gcp = client.post("/plans", json={"cloud": "gcp", "resource": "cluster", "name": "pay"}).json()
    aws = client.post("/plans", json={"cloud": "aws", "resource": "bucket", "name": "pay"}).json()
    azure = client.post("/plans", json={"cloud": "azure", "resource": "cluster", "name": "pay"}).json()
    assert gcp["terraform_type"] == "google_container_cluster"
    assert aws["terraform_type"] == "aws_s3_bucket"
    assert azure["terraform_type"] == "azurerm_kubernetes_cluster"
    assert gcp["applied"] is aws["applied"] is azure["applied"] is False
    assert client.post("/plans", json={"cloud": "onprem", "resource": "cluster", "name": "pay"}).status_code == 422
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /plans` → `create_plan` in [`src/controlplane/main.py`](src/controlplane/main.py#L16).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. Where does state live, and what happens with multiple workers?

Module-level containers include `RESOURCES` in [`src/controlplane/plan.py`](src/controlplane/plan.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `build_plan`?

In [`src/controlplane/plan.py`](src/controlplane/plan.py#L8), `build_plan(cloud, resource, name)` receives the inputs. The function computes these intermediate values:

- `kind = RESOURCES[cloud][resource]`

Its result is defined by:

- `{'cloud': cloud, 'resource': resource, 'name': name, 'terraform_type': kind, 'applied': False}`
