"""
CLI Diagnostic Tool for Testing MySQL Connection
Run with: python db/test_connection.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db.connection import DatabaseManager
from config import DatabaseConfig


def main():
    print("=" * 65)
    print(" Pune Vegetation Monitoring DBMS - Database Connection Diagnostic")
    print("=" * 65)
    print(f"Target Host     : {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
    print(f"Target Database : {DatabaseConfig.NAME}")
    print(f"Target User     : {DatabaseConfig.USER}")
    print(f"Password Set    : {'Yes (Length: ' + str(len(DatabaseConfig.PASSWORD)) + ')' if DatabaseConfig.PASSWORD else 'No (Empty)'}")
    print("-" * 65)
    print("Attempting handshake with MySQL 8 Server...")

    success, info = DatabaseManager.test_connection()

    if success:
        print("[SUCCESS] Connected successfully to MySQL Server!")
        print(f"  - Server Version : {info['version']}")
        print(f"  - Server Time    : {info['server_time']}")
        print(f"  - Tables in DB   : {info['table_count']}")
        print(f"  - Query Latency  : {info['latency_ms']} ms")
        if info['table_count'] == 0:
            print("\n[NOTE] Database exists but currently has 0 tables.")
            print("       Execute 'db/schema.sql' in MySQL Workbench to create the tables.")
        else:
            print("\n[READY] Database is ready for Streamlit application and queries.")
    else:
        print("[FAILED] Could not connect to MySQL Server.")
        print(f"  - Error Code    : {info.get('error_code')}")
        print(f"  - Diagnostic    : {info.get('error_message')}")
        print("\nTroubleshooting Steps:")
        print("1. Verify your MySQL 8 service is running ('Get-Service MySQL80' in PowerShell).")
        print("2. Verify credentials in your '.env' file match your MySQL Workbench user.")
        print("3. Ensure the database 'pune_vegetation_db' was created (see db/schema.sql).")
    print("=" * 65)


if __name__ == "__main__":
    main()
