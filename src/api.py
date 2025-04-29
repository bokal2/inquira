from fastapi import FastAPI
from src.agent.controller import router as agent_router
from src.scripts.controller import router as dev_router


def register_routes(app: FastAPI):
    app.include_router(agent_router)
    app.include_router(dev_router)
