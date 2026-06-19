"""
CloudForge FinOps Platform — FastAPI Backend
Entry point — registers all API routers
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from api import provision, deploy, health, cost, compliance

app = FastAPI(
    title="CloudForge FinOps API",
    description="Cloud-native AWS developer platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(provision.router, prefix="/api/provision", tags=["Provision"])
app.include_router(deploy.router,    prefix="/api/deploy",    tags=["Deploy"])
app.include_router(health.router,    prefix="/api/health",    tags=["Health"])
app.include_router(cost.router,      prefix="/api/cost",      tags=["Cost"])
app.include_router(compliance.router,prefix="/api/compliance",tags=["Compliance"])


@app.get("/")
def root():
    return {
        "service": "CloudForge FinOps",
        "status": "running",
        "version": "1.0.0"
    }