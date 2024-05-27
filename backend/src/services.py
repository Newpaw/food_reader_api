from sqlalchemy.engine.base import Engine
from .logger import setup_logger

logger = setup_logger(__name__)



def get_db_type(engine: Engine) -> str:
    if 'postgresql' in str(engine.url):
        logger.info("PostgreSQL")
        return "PostgreSQL"
    elif 'sqlite' in str(engine.url):
        logger.info("SQLite")
        return "SQLite"
    return "Unknown"