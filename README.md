# Multi-cloud control plane

Level: Advanced+

Skills: GCP, AWS, Azure, Terraform types, APIs

One request names a cloud, a resource (`bucket` or `cluster`), and a name. The response is a plan with the Terraform type for that cloud. `applied` is false. No credential is read.

```bash
pip install -r requirements.txt
pytest -q
```

