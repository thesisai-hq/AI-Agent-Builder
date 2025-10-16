"""
Repository - UPDATED with security validation
"""

from typing import List, Optional, Dict, Any
import json
from contextlib import contextmanager
from agent_builder.repositories.connection import get_db_cursor
from agent_builder.security import validate_table_name
import logging

logger = logging.getLogger(__name__)


class Repository:
    """Simple repository with SQL injection prevention"""

    def __init__(self, db_connection):
        self.db = db_connection
        self._use_postgres = hasattr(db_connection, "cursor")

    def save(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save data to table - WITH VALIDATION"""
        table = validate_table_name(table)

        if self._use_postgres:
            return self._save_postgres(table, data)
        else:
            return self._save_memory(table, data)

    def find_by_id(self, table: str, id: str) -> Optional[Dict[str, Any]]:
        """Find by ID - WITH VALIDATION"""
        table = validate_table_name(table)

        if self._use_postgres:
            return self._find_postgres(table, id)
        else:
            return self._find_memory(table, id)

    def find_all(self, table: str, filters: Dict = None) -> List[Dict[str, Any]]:
        """Find all - WITH VALIDATION"""
        table = validate_table_name(table)

        if self._use_postgres:
            return self._find_all_postgres(table, filters)
        else:
            return self._find_all_memory(table, filters)

    def delete(self, table: str, id: str) -> bool:
        """Delete - WITH VALIDATION"""
        table = validate_table_name(table)

        if self._use_postgres:
            return self._delete_postgres(table, id)
        else:
            return self._delete_memory(table, id)

    # ========================================================================
    # In-Memory Implementation (unchanged)
    # ========================================================================

    def _save_memory(self, table: str, data: Dict) -> Dict:
        """Save to in-memory dict"""
        if table not in self.db:
            self.db[table] = {}

        id = data.get("id")
        self.db[table][id] = data
        return data

    def _find_memory(self, table: str, id: str) -> Optional[Dict]:
        """Find in memory"""
        return self.db.get(table, {}).get(id)

    def _find_all_memory(self, table: str, filters: Dict = None) -> List[Dict]:
        """Find all in memory"""
        items = list(self.db.get(table, {}).values())

        if filters:
            for key, value in filters.items():
                items = [i for i in items if i.get(key) == value]

        return items

    def _delete_memory(self, table: str, id: str) -> bool:
        """Delete from memory"""
        if table in self.db and id in self.db[table]:
            del self.db[table][id]
            return True
        return False

    # ========================================================================
    # PostgreSQL Implementation - UPDATED to use connection pool
    # ========================================================================

    def _save_postgres(self, table: str, data: Dict) -> Dict:
        """Save to PostgreSQL - Uses connection pool"""
        import psycopg2.extras

        with get_db_cursor() as cursor:
            if cursor is None:
                return data

            # Prepare data
            prepared_data = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    prepared_data[key] = psycopg2.extras.Json(value)
                else:
                    prepared_data[key] = value

            # Build query
            columns = list(prepared_data.keys())
            values = list(prepared_data.values())
            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join(columns)

            query = f"""
                INSERT INTO {table} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT (id) DO UPDATE SET
                {', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != 'id'])}
                RETURNING *
            """

            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                return dict(zip(columns, result))
            return data

    def _find_postgres(self, table: str, id: str) -> Optional[Dict]:
        """Find in PostgreSQL - Uses connection pool"""
        with get_db_cursor() as cursor:
            if cursor is None:
                return None

            cursor.execute(f"SELECT * FROM {table} WHERE id = %s", (id,))
            result = cursor.fetchone()

            if not result:
                return None

            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))

    def _find_all_postgres(self, table: str, filters: Dict = None) -> List[Dict]:
        """Find all in PostgreSQL - Uses connection pool"""
        with get_db_cursor() as cursor:
            if cursor is None:
                return []

            query = f"SELECT * FROM {table}"
            params = []

            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(f"{key} = %s")
                    params.append(value)
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, params)
            results = cursor.fetchall()

            if not results:
                return []

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]

    def _delete_postgres(self, table: str, id: str) -> bool:
        """Delete from PostgreSQL - Uses connection pool"""
        with get_db_cursor() as cursor:
            if cursor is None:
                return False

            cursor.execute(f"DELETE FROM {table} WHERE id = %s", (id,))
            return cursor.rowcount > 0
