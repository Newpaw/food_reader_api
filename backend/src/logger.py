import logging
from .config import settings

def setup_logger(name: str) -> logging.Logger:
    log_level = settings.LOG_LEVEL
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Set up basic configuration for your logger
    logging.basicConfig(
        level=numeric_level,
        format="%(levelname)s:     %(asctime)s - %(name)s - %(message)s"
    )

    # Create a logger object
    logger = logging.getLogger(name)
    logger.info(f"Log level set to {log_level}")

    # Set log level for third-party libraries to WARNING or ERROR
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("multipart.multipart").setLevel(logging.WARNING)



    return logger
