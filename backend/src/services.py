from sqlalchemy.engine.base import Engine

def get_db_type(engine: Engine) -> str:
    if 'postgresql' in str(engine.url):
        return "PostgreSQL"
    elif 'sqlite' in str(engine.url):
        return "SQLite"
    return "Unknown"