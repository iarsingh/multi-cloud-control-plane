from fastapi.testclient import TestClient

from controlplane.main import app

client = TestClient(app)


def test_three_clouds_share_a_plan_and_nothing_is_applied():
    gcp = client.post("/plans", json={"cloud": "gcp", "resource": "cluster", "name": "pay"}).json()
    aws = client.post("/plans", json={"cloud": "aws", "resource": "bucket", "name": "pay"}).json()
    azure = client.post("/plans", json={"cloud": "azure", "resource": "cluster", "name": "pay"}).json()
    assert gcp["terraform_type"] == "google_container_cluster"
    assert aws["terraform_type"] == "aws_s3_bucket"
    assert azure["terraform_type"] == "azurerm_kubernetes_cluster"
    assert gcp["applied"] is aws["applied"] is azure["applied"] is False
    assert client.post("/plans", json={"cloud": "onprem", "resource": "cluster", "name": "pay"}).status_code == 422
