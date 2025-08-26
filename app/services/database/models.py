from typing import Optional

from sqlmodel import Field, SQLModel

from app.services.database.session import engine


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None


# -------------------------
# Configuration function
# -------------------------
def configure():
    """
    Create all tables in the database.
    Seed data will be applied via event listeners if tables are newly created.
    After seeding, reset all sequences to avoid duplicate key errors.
    I have commented out the reset_all_sequences call to avoid unnecessary loading when the application starts.
    """
    SQLModel.metadata.create_all(bind=engine)
