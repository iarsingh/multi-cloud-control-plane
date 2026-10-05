from controlplane.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from controlplane.plan import RESOURCES, build_plan

app = FastAPI(title="Multi-cloud control plane")
app.include_router(ops_router, prefix="/v1")


class PlanRequest(BaseModel):
    cloud: str
    resource: str
    name: str


@app.post("/plans")
def create_plan(body: PlanRequest):
    if body.cloud not in RESOURCES:
        raise HTTPException(status_code=422, detail="cloud must be gcp, aws, or azure")
    if body.resource not in RESOURCES[body.cloud]:
        raise HTTPException(status_code=422, detail="resource must be bucket or cluster")
    return build_plan(body.cloud, body.resource, body.name)
