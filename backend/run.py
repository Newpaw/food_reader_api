from src.fastapi_module import create_app


backend = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:backend", host="0.0.0.0", port=8000, reload=True)
