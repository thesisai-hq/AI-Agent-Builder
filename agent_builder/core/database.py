"""Database connection and pooling"""

from contextlib import contextmanager
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class DatabasePool:
    def __init__(self, config):
        self.config = config
        self._pool = None
        if config.is_postgres:
            self._init_postgres_pool()
    
    def _init_postgres_pool(self):
        try:
            from psycopg2.pool import SimpleConnectionPool
            from urllib.parse import urlparse
            
            parsed = urlparse(self.config.url)
            self._pool = SimpleConnectionPool(
                minconn=self.config.min_connections,
                maxconn=self.config.max_connections,
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path.lstrip("/"),
                user=parsed.username,
                password=parsed.password,
            )
            logger.info(f"✅ Database pool initialized ({self.config.min_connections}-{self.config.max_connections} connections)")
        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise
    
    @contextmanager
    def get_cursor(self):
        if not self._pool:
            yield None
            return
        conn = None
        try:
            conn = self._pool.getconn()
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                self._pool.putconn(conn)
    
    def close(self):
        if self._pool:
            self._pool.closeall()
            logger.info("✅ Database pool closed")
    
    def create_tables(self):
        if not self._pool:
            return
        with self.get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id VARCHAR(255) PRIMARY KEY,
                    ticker VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    signals JSONB DEFAULT '[]',
                    consensus JSONB,
                    error TEXT,
                    started_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_ticker ON analyses(ticker)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_status ON analyses(status)")
            logger.info("✅ Database tables ready")


class Database:
    def __init__(self, pool):
        self.pool = pool
    
    def execute(self, query: str, params: tuple = None) -> list:
        with self.pool.get_cursor() as cursor:
            if not cursor:
                return []
            cursor.execute(query, params or ())
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []
    
    def execute_one(self, query: str, params: tuple = None) -> Optional[dict]:
        results = self.execute(query, params)
        return results[0] if results else None
    
    def execute_value(self, query: str, params: tuple = None, default: Any = None) -> Any:
        with self.pool.get_cursor() as cursor:
            if not cursor:
                return default
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result[0] if result else default
    
    def save_analysis(self, data: dict) -> dict:
        import json
        query = """
            INSERT INTO analyses (id, ticker, status, signals, consensus, error, started_at, completed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                status = EXCLUDED.status, signals = EXCLUDED.signals,
                consensus = EXCLUDED.consensus, error = EXCLUDED.error,
                completed_at = EXCLUDED.completed_at
            RETURNING *
        """
        result = self.execute_one(query, (
            data['id'], data['ticker'], data['status'],
            json.dumps(data.get('signals', [])),
            json.dumps(data.get('consensus')) if data.get('consensus') else None,
            data.get('error'), data['started_at'], data.get('completed_at'),
        ))
        return result or data
    
    def get_analysis(self, analysis_id: str):
        return self.execute_one("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
