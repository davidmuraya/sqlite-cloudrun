from pathlib import Path

from sqlalchemy import event
from sqlmodel import Session, create_engine

from app.config.main import get_settings

settings = get_settings()

# Check for required environment variables
required_vars = [settings.DB]
if not all(required_vars):
    raise ValueError("Database environment variables are missing or invalid. Please check your .env file.")


# Database Configuration
DATABASE_PATH = Path(settings.DB)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False, "timeout": 30}  # When set to False: The connection can be shared across multiple threads.

engine = create_engine(DATABASE_URL, echo=False, connect_args=CONNECT_ARGS)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA cache_size=10000;")  # Increase cache size (in pages)
    cursor.execute("PRAGMA temp_store=FILE;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.close()


def get_db():
    """Yields a SQLModel Session instance."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
