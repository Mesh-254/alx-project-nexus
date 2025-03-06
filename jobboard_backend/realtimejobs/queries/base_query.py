import os
import pymysql #type: ignore
import aiomysql #type: ignore
import functools
import hashlib
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global cache dictionary
query_cache = {}

class DatabaseConnection:
    """Manages synchronous database connections using pymysql."""
    
    def __init__(self, db_host=None, db_user=None, db_password=None, db_database=None):
        self.db_host = db_host or os.getenv('DB_HOST')
        self.db_user = db_user or os.getenv('DB_USER')
        self.db_password = db_password or os.getenv('DB_PASSWORD')
        self.db_name = db_database or os.getenv('DB_NAME')
        self.conn = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"[ERROR] Database Error: {exc_type}, {exc_val}")
            return False
        return True

class AsyncDatabaseConnection:
    """Manages asynchronous database connections using aiomysql."""
    
    async def __aenter__(self):
        self.pool = await aiomysql.create_pool(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            cursorclass=aiomysql.DictCursor
        )
        self.conn = await self.pool.acquire()
        self.cursor = await self.conn.cursor()
        return self.cursor

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await self.conn.ensure_closed()
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
        if exc_type:
            print(f"[ERROR] Database Error: {exc_type}, {exc_val}")
            return False
        return True

def cache_query(func):
    """Caches query results to reduce redundant database calls."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", "")
        params = kwargs.get("params", ())
        cache_key = hashlib.sha256((query + json.dumps(params, sort_keys=True)).encode()).hexdigest()

        if cache_key in query_cache:
            print(f"[CACHE] Hit for query: {query}")
            return query_cache[cache_key]

        result = func(*args, **kwargs)
        query_cache[cache_key] = result
        print(f"[CACHE] Stored query: {query}")
        return result
    return wrapper

class BaseQuery:
    """Base class for handling database queries with caching and async support."""
    
    @staticmethod
    @cache_query
    def fetch_all(query, params=()):
        with DatabaseConnection() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    @cache_query
    def fetch_one(query, params=()):
        with DatabaseConnection() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    @staticmethod
    def execute_query(query, params=()):
        """Executes INSERT, UPDATE, DELETE queries."""
        with DatabaseConnection() as cursor:
            cursor.execute(query, params)
            cursor.connection.commit()
            print(f"[INFO] Executed: {query} with params: {params}")

    @staticmethod
    async def async_fetch_all(query, params=()):
        """Handles async fetch for SELECT queries."""
        async with AsyncDatabaseConnection() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

    @staticmethod
    async def async_fetch_one(query, params=()):
        """Handles async fetch for a single record."""
        async with AsyncDatabaseConnection() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()
