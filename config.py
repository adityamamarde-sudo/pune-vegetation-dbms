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

# Streamlit Community Cloud secrets fallback
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            if isinstance(v, (str, int, float, bool)):
                os.environ.setdefault(k, str(v))
except Exception:
    pass



class DatabaseConfig:
    """MySQL 8 Database configuration parameters."""
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", "3306"))
    NAME: str = os.getenv("DB_NAME", "pune_vegetation_db")
    USER: str = os.getenv("DB_USER", "root")
    PASSWORD: str = os.getenv("DB_PASSWORD", "")
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    POOL_NAME: str = os.getenv("DB_POOL_NAME", "pune_veg_pool")

    @classmethod
    def get_sqlalchemy_url(cls) -> str:
        """Returns SQLAlchemy connection URI using PyMySQL."""
        from urllib.parse import quote_plus
        safe_pass = quote_plus(cls.PASSWORD)
        return f"mysql+pymysql://{cls.USER}:{safe_pass}@{cls.HOST}:{cls.PORT}/{cls.NAME}?charset=utf8mb4"


class GEEConfig:
    """Google Earth Engine configuration parameters."""
    PROJECT_ID: str = os.getenv("GEE_PROJECT_ID", "")
    AUTH_MODE: str = os.getenv("GEE_AUTH_MODE", "local")
    COLLECTION_ID: str = "COPERNICUS/S2_SR_HARMONIZED"
    NIR_BAND: str = "B8"
    RED_BAND: str = "B4"


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
