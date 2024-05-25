from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

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
    origins = ["*"]  # Allow all origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from .routes import setup_routes
    setup_routes(app)

    # Vytvoření tabulek v databázi podle modelů
    Base.metadata.create_all(bind=engine)

    return app
