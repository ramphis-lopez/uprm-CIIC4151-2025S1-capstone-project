import psycopg2
import bcrypt
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()


def load_db():
    """
    Establish and return a connection to the PostgreSQL database.

    Returns:
        psycopg2.connection: Database connection object
    """
    try:
        # Prefer Heroku DATABASE_URL if it exists
        database_url = os.getenv("DATABASE_URL")

        if database_url:
            # Heroku case
            return psycopg2.connect(database_url, connect_timeout=5)

        # Local development (fallback to individual vars)
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            connect_timeout=5,
        )
        print("Database connection established successfully")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def close_db(conn, cursor):
    """
    Close database connection and cursor.

    Args:
        conn: Database connection
        cursor: Database cursor
    """
    if cursor:
        cursor.close()
    if conn:
        conn.commit()
        conn.close()
        print("Database connection closed")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password (str): Plain text password to verify
        hashed (str): Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False
