from app.config.main import get_settings
from app.services.database.models import configure

settings = get_settings()


async def on_start_up() -> None:
    """
    Function to initialize the database.
    """
    pass
    # configure()


async def on_shutdown() -> None:
    """
    Function to close the http client and memcached client.
    """
    pass
