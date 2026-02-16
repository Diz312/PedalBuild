#!/usr/bin/env python3
"""
Database setup script for PedalBuild.

Reads src/db/schema.sql and initializes data/db/pedalbuild.db.
Safe to run multiple times - will not overwrite existing database unless --force flag is used.

Usage:
    python scripts/setup-db.py              # Create database if not exists
    python scripts/setup-db.py --force      # Recreate database (DESTRUCTIVE)
    python scripts/setup-db.py --check      # Check if database exists
"""

import argparse
import logging
import sqlite3
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = PROJECT_ROOT / "src" / "db" / "schema.sql"
DB_DIR = PROJECT_ROOT / "data" / "db"
DB_PATH = DB_DIR / "pedalbuild.db"


def check_database_exists() -> bool:
    """Check if database file exists and has tables."""
    if not DB_PATH.exists():
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = cursor.fetchall()
        conn.close()

        if not tables:
            logger.warning("Database file exists but contains no tables")
            return False

        logger.info(f"Database exists with {len(tables)} tables")
        return True

    except sqlite3.Error as e:
        logger.error(f"Error checking database: {e}")
        return False


def create_database(force: bool = False) -> bool:
    """
    Create database from schema file.

    Args:
        force: If True, delete existing database before creating new one

    Returns:
        True if successful, False otherwise
    """
    # Check if database already exists
    if DB_PATH.exists():
        if not force:
            logger.warning(f"Database already exists at {DB_PATH}")
            logger.warning("Use --force to recreate (will delete all data)")
            return False
        else:
            logger.warning("Deleting existing database (--force specified)")
            DB_PATH.unlink()

    # Read schema file
    if not SCHEMA_PATH.exists():
        logger.error(f"Schema file not found: {SCHEMA_PATH}")
        return False

    logger.info(f"Reading schema from {SCHEMA_PATH}")
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    # Create database directory if needed
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Create and initialize database
    try:
        logger.info(f"Creating database at {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")

        # Execute schema
        cursor.executescript(schema_sql)
        conn.commit()

        # Verify tables were created
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]

        logger.info(f"Successfully created {len(tables)} tables:")
        for name in sorted(table_names):
            logger.info(f"  - {name}")

        # Verify views were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = cursor.fetchall()
        if views:
            logger.info(f"Created {len(views)} views:")
            for view in views:
                logger.info(f"  - {view[0]}")

        # Verify triggers were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
        triggers = cursor.fetchall()
        if triggers:
            logger.info(f"Created {len(triggers)} triggers")

        conn.close()
        logger.info("Database initialization complete!")
        return True

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        if DB_PATH.exists():
            DB_PATH.unlink()
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if DB_PATH.exists():
            DB_PATH.unlink()
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize PedalBuild SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recreate database even if it exists (DESTRUCTIVE)",
    )
    parser.add_argument(
        "--check", action="store_true", help="Check if database exists and exit"
    )

    args = parser.parse_args()

    if args.check:
        exists = check_database_exists()
        sys.exit(0 if exists else 1)

    success = create_database(force=args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
