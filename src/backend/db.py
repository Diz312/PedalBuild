"""
Database connection utilities for PedalBuild.

Provides:
- Connection pooling with context managers
- FastAPI dependency injection
- Transaction management
- Error handling
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

logger = logging.getLogger(__name__)

# Database configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "db" / "pedalbuild.db"


class DatabaseError(Exception):
    """Base exception for database errors."""

    pass


class Database:
    """
    Database connection manager.

    Provides connection pooling, context managers, and thread-safe access.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database connection manager.

        Args:
            db_path: Path to SQLite database file. Defaults to project database.
        """
        self.db_path = db_path or DB_PATH

        if not self.db_path.exists():
            raise DatabaseError(
                f"Database not found at {self.db_path}. Run 'npm run setup:db' first."
            )

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a new database connection.

        Returns:
            SQLite connection with foreign keys enabled and row factory configured.
        """
        try:
            conn = sqlite3.connect(str(self.db_path), check_same_thread=False)

            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")

            # Use Row factory for dict-like access
            conn.row_factory = sqlite3.Row

            return conn

        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise DatabaseError(f"Database connection failed: {e}") from e

    @contextmanager
    def get_cursor(self, commit: bool = False) -> Generator[sqlite3.Cursor, None, None]:
        """
        Context manager for database cursor with automatic cleanup.

        Args:
            commit: If True, commit transaction on success. Rollback on error.

        Yields:
            Database cursor

        Example:
            with db.get_cursor(commit=True) as cursor:
                cursor.execute("INSERT INTO components ...")
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            yield cursor

            if commit:
                conn.commit()
                logger.debug("Transaction committed")

        except sqlite3.Error as e:
            if commit:
                conn.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
            raise DatabaseError(f"Database operation failed: {e}") from e

        finally:
            cursor.close()
            conn.close()

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        """
        Context manager for database transactions.

        Automatically commits on success, rolls back on error.

        Yields:
            Database cursor

        Example:
            with db.transaction() as cursor:
                cursor.execute("INSERT INTO components ...")
                cursor.execute("UPDATE projects ...")
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            yield cursor
            conn.commit()
            logger.debug("Transaction committed")

        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction rolled back: {e}")
            raise

        finally:
            cursor.close()
            conn.close()

    def execute_query(
        self, query: str, params: tuple = (), fetch_one: bool = False
    ) -> list[sqlite3.Row] | sqlite3.Row | None:
        """
        Execute a SELECT query and return results.

        Args:
            query: SQL query
            params: Query parameters
            fetch_one: If True, return single row. If False, return all rows.

        Returns:
            Query results as Row objects, single Row, or None
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)

            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def execute_update(
        self, query: str, params: tuple = ()
    ) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of affected rows
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def execute_many(
        self, query: str, params_list: list[tuple]
    ) -> int:
        """
        Execute multiple INSERT/UPDATE operations efficiently.

        Args:
            query: SQL query
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

    def check_health(self) -> bool:
        """
        Check if database is accessible and healthy.

        Returns:
            True if database is healthy, False otherwise
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database instance
_db_instance: Optional[Database] = None


def get_database() -> Database:
    """
    Get global database instance (singleton pattern).

    Returns:
        Database instance

    Raises:
        DatabaseError: If database cannot be initialized
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = Database()

    return _db_instance


# FastAPI dependency
def get_db() -> Generator[Database, None, None]:
    """
    FastAPI dependency for database injection.

    Yields:
        Database instance

    Example:
        @app.get("/components")
        def list_components(db: Database = Depends(get_db)):
            return db.execute_query("SELECT * FROM components")
    """
    db = get_database()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database dependency error: {e}")
        raise


def row_to_dict(row: sqlite3.Row) -> dict:
    """
    Convert SQLite Row to dictionary.

    Args:
        row: SQLite Row object

    Returns:
        Dictionary with column names as keys
    """
    return {key: row[key] for key in row.keys()}


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    """
    Convert list of SQLite Rows to list of dictionaries.

    Args:
        rows: List of SQLite Row objects

    Returns:
        List of dictionaries
    """
    return [row_to_dict(row) for row in rows]
