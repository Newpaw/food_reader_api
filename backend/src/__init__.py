from fastapi import FastAPI
from .config import settings

def create_app() -> FastAPI:
    """
    Application factory function. This function creates and configures
    an instance of the FastAPI application.
    """

    app = FastAPI(
        title="Food recognition API",
        version="0.0.2",
        description="An API for food recognition",
    )

    from .routes import setup_routes
    setup_routes(app)

    return app
