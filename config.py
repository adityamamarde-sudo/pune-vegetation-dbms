"""
Application Configuration Module
Reads settings from environment variables and provides structured config objects.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent

# Load .env if present
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    # Also attempt standard load_dotenv() from CWD
    load_dotenv()

def get_secret(key: str, default=None):
    """Retrieves secret from st.secrets if running on Streamlit Cloud, else from env."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


class DatabaseConfig:
    """MySQL 8 Database configuration parameters."""
    HOST: str = str(get_secret("DB_HOST", "localhost"))
    PORT: int = int(get_secret("DB_PORT", 3306))
    NAME: str = str(get_secret("DB_NAME", "pune_vegetation_db"))
    USER: str = str(get_secret("DB_USER", "root"))
    PASSWORD: str = str(get_secret("DB_PASSWORD", ""))
    POOL_SIZE: int = int(get_secret("DB_POOL_SIZE", 5))
    POOL_NAME: str = str(get_secret("DB_POOL_NAME", "pune_veg_pool"))

    @classmethod
    def reload(cls):
        cls.HOST = str(get_secret("DB_HOST", "localhost"))
        cls.PORT = int(get_secret("DB_PORT", 3306))
        cls.NAME = str(get_secret("DB_NAME", "pune_vegetation_db"))
        cls.USER = str(get_secret("DB_USER", "root"))
        cls.PASSWORD = str(get_secret("DB_PASSWORD", ""))
        cls.POOL_SIZE = int(get_secret("DB_POOL_SIZE", 5))

    @classmethod
    def get_sqlalchemy_url(cls) -> str:
        """Returns SQLAlchemy connection URI using PyMySQL."""
        cls.reload()
        from urllib.parse import quote_plus
        safe_pass = quote_plus(cls.PASSWORD)
        return f"mysql+pymysql://{cls.USER}:{safe_pass}@{cls.HOST}:{cls.PORT}/{cls.NAME}?charset=utf8mb4"


class GEEConfig:
    """Google Earth Engine configuration parameters."""
    PROJECT_ID: str = str(get_secret("GEE_PROJECT_ID", ""))
    AUTH_MODE: str = str(get_secret("GEE_AUTH_MODE", "local"))
    COLLECTION_ID: str = "COPERNICUS/S2_SR_HARMONIZED"
    NIR_BAND: str = "B8"
    RED_BAND: str = "B4"

    @classmethod
    def reload(cls):
        cls.PROJECT_ID = str(get_secret("GEE_PROJECT_ID", ""))
        cls.AUTH_MODE = str(get_secret("GEE_AUTH_MODE", "local"))


def reload_configs():
    DatabaseConfig.reload()
    GEEConfig.reload()



class AppConfig:
    """General Application and Map settings."""
    ENV: str = os.getenv("APP_ENV", "development")
    MAX_STUDY_AREA_SQ_KM: float = float(os.getenv("MAX_STUDY_AREA_SQ_KM", "5000.0"))
    DEFAULT_MAP_LAT: float = float(os.getenv("DEFAULT_MAP_LAT", "18.520430"))
    DEFAULT_MAP_LON: float = float(os.getenv("DEFAULT_MAP_LON", "73.856744"))
    DEFAULT_MAP_ZOOM: int = int(os.getenv("DEFAULT_MAP_ZOOM", "10"))

    # Preset Study Areas directory
    DATA_DIR: Path = BASE_DIR / "data"
    DOCS_DIR: Path = BASE_DIR / "docs"
