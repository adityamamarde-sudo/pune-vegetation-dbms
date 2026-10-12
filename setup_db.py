"""
Interactive Database Setup & Migration Script
Executes db/schema.sql and db/seed_demo_data.sql into your local MySQL 8 Server.
Run with: python setup_db.py
"""

import sys
import os
import getpass
from pathlib import Path
import pymysql

# Add root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DatabaseConfig


def split_sql_statements(sql_text: str):
    """
    Splits SQL script into individual executable statements,
    properly ignoring comments and empty lines.
    """
    statements = []
    current = []
    in_trigger = False

    for line in sql_text.splitlines():
        trimmed = line.strip()
        # Skip pure comments
        if trimmed.startswith("--") or not trimmed:
            continue

        if "DELIMITER $$" in line:
            in_trigger = True
            continue
        if "DELIMITER ;" in line:
            in_trigger = False
            if current:
                stmt = "\n".join(current).strip()
                if stmt:
                    statements.append(stmt)
                current = []
            continue

        current.append(line)

        if not in_trigger and trimmed.endswith(";"):
            stmt = "\n".join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []

    if current:
        stmt = "\n".join(current).strip()
        if stmt:
            statements.append(stmt)

    return statements


def execute_sql_file(conn, file_path: Path):
    """Executes all statements in a given SQL script."""
    print(f"\n>> Executing script: {file_path.name}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    statements = split_sql_statements(content)
    with conn.cursor() as cursor:
        for idx, stmt in enumerate(statements, 1):
            # Clean trailing semicolon or delimiter
            clean_stmt = stmt.strip()
            if clean_stmt.endswith("$$"):
                clean_stmt = clean_stmt[:-2].strip()
            if not clean_stmt:
                continue
            try:
                cursor.execute(clean_stmt)
            except Exception as e:
                print(f"   [Error in statement #{idx}]: {e}")
                raise
    conn.commit()
    print(f"   [Done] Successfully executed {len(statements)} statements from {file_path.name}.")


def main():
    print("=" * 65)
    print(" Pune Vegetation DBMS - Automated Database Setup Tool")
    print("=" * 65)

    host = DatabaseConfig.HOST
    port = DatabaseConfig.PORT
    user = DatabaseConfig.USER
    password = DatabaseConfig.PASSWORD

    # If password in .env is default/empty, prompt the user
    if not password or password == "replace_with_your_mysql_password":
        print(f"Connecting to MySQL at {host}:{port} as user '{user}'...")
        try:
            password = getpass.getpass("Enter your MySQL password (input will be hidden): ")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            return

    # 1. Connect without selecting database to run CREATE DATABASE IF NOT EXISTS
    print("\n[Step 1/3] Connecting to MySQL Server...")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4",
            autocommit=False,
            connect_timeout=10,
        )
        print("[SUCCESS] MySQL handshake established!")
    except pymysql.err.OperationalError as e:
        code, msg = e.args if len(e.args) == 2 else (0, str(e))
        print(f"\n[FAILED] Connection failed (Code {code}): {msg}")
        if code == 1045:
            print("Please double check your MySQL root password.")
        return

    # 2. Execute schema.sql
    schema_path = PROJECT_ROOT / "db" / "schema.sql"
    seed_path = PROJECT_ROOT / "db" / "seed_demo_data.sql"

    try:
        print("\n[Step 2/3] Initializing schema (tables, views, indexes, triggers)...")
        execute_sql_file(conn, schema_path)

        print("\n[Step 3/3] Populating Pune study-area presets and sample demo runs...")
        execute_sql_file(conn, seed_path)

        # 3. Update .env with working password if different
        env_path = PROJECT_ROOT / ".env"
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            updated_lines = []
            for line in lines:
                if line.startswith("DB_PASSWORD="):
                    updated_lines.append(f"DB_PASSWORD={password}\n")
                else:
                    updated_lines.append(line)
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(updated_lines)
            print("\n[INFO] Saved password to .env for application use.")

        # 4. Final verification
        with conn.cursor() as cursor:
            cursor.execute("USE pune_vegetation_db;")
            cursor.execute("SELECT COUNT(*) AS c FROM study_areas;")
            areas_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) AS c FROM analysis_runs;")
            runs_count = cursor.fetchone()[0]

        conn.close()

        print("\n" + "=" * 65)
        print(" [SETUP COMPLETE] Database is fully operational!")
        print(f"  - Database Name    : pune_vegetation_db")
        print(f"  - Study Areas Seeded: {areas_count} preset regions (Pune, Mulshi, Haveli, etc.)")
        print(f"  - Sample Runs      : {runs_count} demo analyses")
        print("=" * 65)
        print("\nYou can now open MySQL Workbench to inspect the database,")
        print("or run 'python db/test_connection.py' anytime to verify.")

    except Exception as e:
        print(f"\n[ERROR] Setup encountered an issue: {e}")
        conn.rollback()
        conn.close()


if __name__ == "__main__":
    main()
