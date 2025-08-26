from app.config.main import get_settings
from app.services.database.models import configure
from app.services.database.session import engine

settings = get_settings()


async def on_start_up() -> None:
    """
    Function to initialize the database.
    """
    configure()


async def on_shutdown() -> None:
    """
    Function to close the http client and memcached client.
    It also performs a database checkpoint to ensure all data from the WAL file is written to the main database file.
    """
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA wal_checkpoint(TRUNCATE);")
