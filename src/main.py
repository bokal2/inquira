from fastapi import FastAPI, Request, Response
import logging
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.db.core import engine, Base
from src.logging import setup_logging
from src.api import register_routes
from src.rate_limiting import limiter
from src.entities.customer import Customer, Order, OrderItem, Product


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized.")

    yield  # App runs here

    print("App shutting down.")


app = FastAPI(
    title="Business Intelligence Chatbot",
    description=(
        "An AI-powered chatbot for interacting with the database using natural language."
    ),
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure allowed origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_and_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id

    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host,
            "headers": dict(request.headers),
        },
    )

    response: Response = await call_next(request)

    logger.info(
        "Outgoing response",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "url": str(request.url),
        },
    )

    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/healthy")
def health():
    return {"status": "ok"}


Instrumentator().instrument(app).expose(app)

register_routes(app)
