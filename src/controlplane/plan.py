RESOURCES = {
    "gcp": {"bucket": "google_storage_bucket", "cluster": "google_container_cluster"},
    "aws": {"bucket": "aws_s3_bucket", "cluster": "aws_eks_cluster"},
    "azure": {"bucket": "azurerm_storage_account", "cluster": "azurerm_kubernetes_cluster"},
}


def build_plan(cloud, resource, name):
    kind = RESOURCES[cloud][resource]
    return {
        "cloud": cloud,
        "resource": resource,
        "name": name,
        "terraform_type": kind,
        "applied": False,
    }
