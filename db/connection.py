"""
MySQL Database Connection Module
Provides connection pooling, raw connections, SQLAlchemy engine, and connectivity health tests.
Does not log or expose raw passwords.
"""

import time
from typing import Optional, Dict, Any, Tuple
import pymysql
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import DatabaseConfig


class DatabaseManager:
    """Manages connections to MySQL 8 database."""

    _engine: Optional[Engine] = None

    @classmethod
    def get_raw_connection(cls, use_database: bool = True):
        """
        Creates a raw PyMySQL connection.
        If use_database is False, connects to the server without selecting a DB
        (useful for schema creation or initialization).
        """
        return pymysql.connect(
            host=DatabaseConfig.HOST,
            port=DatabaseConfig.PORT,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.NAME if use_database else None,
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False,
            connect_timeout=10,
        )

    @classmethod
    def get_engine(cls) -> Engine:
        """Returns or creates a cached SQLAlchemy engine with connection pooling."""
        if cls._engine is None:
            url = DatabaseConfig.get_sqlalchemy_url()
            cls._engine = create_engine(
                url,
                pool_size=DatabaseConfig.POOL_SIZE,
                max_overflow=10,
                pool_recycle=3600,
                pool_pre_ping=True,
                echo=False,
            )
        return cls._engine

    @classmethod
    def test_connection(cls) -> Tuple[bool, Dict[str, Any]]:
        """
        Tests the MySQL database connection without exposing sensitive credentials.
        Returns:
            (success: bool, info_dict: dict)
        """
        start_time = time.time()
        try:
            conn = cls.get_raw_connection(use_database=True)
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION() AS version, DATABASE() AS db, NOW() AS server_time;")
                row = cursor.fetchone()

                # Also check total table count
                cursor.execute(
                    """
                    SELECT COUNT(*) AS table_count
                    FROM information_schema.tables
                    WHERE table_schema = %s;
                    """,
                    (DatabaseConfig.NAME,),
                )
                tables_row = cursor.fetchone()

            conn.close()
            latency_ms = round((time.time() - start_time) * 1000, 2)

            return True, {
                "status": "connected",
                "host": DatabaseConfig.HOST,
                "port": DatabaseConfig.PORT,
                "database": DatabaseConfig.NAME,
                "user": DatabaseConfig.USER,
                "version": row.get("version") if row else "Unknown",
                "server_time": str(row.get("server_time")) if row else "Unknown",
                "table_count": tables_row.get("table_count", 0) if tables_row else 0,
                "latency_ms": latency_ms,
            }
        except pymysql.err.OperationalError as e:
            code, msg = e.args if len(e.args) == 2 else (0, str(e))
            # Friendly diagnosis without password leakage
            friendly_hint = ""
            if code == 1045:
                friendly_hint = (
                    f"Access denied for user '{DatabaseConfig.USER}'. "
                    "Check your DB_USER and DB_PASSWORD in .env."
                )
            elif code == 1049:
                friendly_hint = (
                    f"Database '{DatabaseConfig.NAME}' does not exist yet. "
                    "Run db/schema.sql in MySQL Workbench to create it."
                )
            elif code == 2003:
                friendly_hint = (
                    f"Cannot connect to MySQL server at {DatabaseConfig.HOST}:{DatabaseConfig.PORT}. "
                    "Ensure MySQL service (MySQL80) is started."
                )
            else:
                friendly_hint = str(msg)

            return False, {
                "status": "error",
                "error_code": code,
                "error_message": friendly_hint,
                "host": DatabaseConfig.HOST,
                "port": DatabaseConfig.PORT,
                "database": DatabaseConfig.NAME,
                "user": DatabaseConfig.USER,
            }
        except Exception as e:
            return False, {
                "status": "error",
                "error_code": 0,
                "error_message": str(e),
                "host": DatabaseConfig.HOST,
                "port": DatabaseConfig.PORT,
            }
