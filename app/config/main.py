"""
This file contains all project configs read from env file.
"""

from enum import Enum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentEnum(str, Enum):
    TEST = "TEST"
    PRODUCTION = "PRODUCTION"


class Settings(BaseSettings):
    # Environment settings
    DEBUG: bool = Field(default=False, validation_alias="DEBUG", alias_priority=2)
    RELOAD: bool = Field(default=False, validation_alias="RELOAD", alias_priority=2)
    ENVIRONMENT: str = Field(default=EnvironmentEnum.TEST, validation_alias="ENVIRONMENT", alias_priority=2)

    # db path
    DB: str = Field(default="", validation_alias="DB", alias_priority=2)

    # Application settings
    LOGLEVEL: str = Field(default="INFO", validation_alias="LOGLEVEL", alias_priority=2)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()
