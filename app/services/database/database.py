from pathlib import Path

from sqlmodel import Session, create_engine

from app.config.main import get_settings

settings = get_settings()

# Database Configuration
DATABASE_PATH = Path(settings.DB)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, connect_args=CONNECT_ARGS)


def get_db():
    """Yields a SQLModel Session instance."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
