import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

conn = psycopg2.connect(**Config.DB_PARAMS)
cur = conn.cursor(cursor_factory=RealDictCursor)

def get_cursor():
    return conn.cursor(cursor_factory=RealDictCursor)

def commit():
    conn.commit()