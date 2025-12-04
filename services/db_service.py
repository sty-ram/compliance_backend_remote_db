import mysql.connector

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ----------------------------
# USER FUNCTIONS
# ----------------------------

def create_user(username, password_hash):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, password) 
        VALUES (%s, %s)
    """, (username, password_hash))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success"}


def fetch_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {"username": row[0], "password": row[1]}
    return None


# ----------------------------
# IMAGE FUNCTIONS
# ----------------------------

def upload_image_to_db(username, file, doc_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO images (username, doc_type, filename, filedata)
        VALUES (%s, %s, %s, %s)
    """, (username, doc_type, file.filename, file.read()))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success"}


def fetch_user_images(username, doc_type=None):
    conn = get_connection()
    cur = conn.cursor()

    if doc_type:
        cur.execute("""
            SELECT filename FROM images 
            WHERE username = %s AND doc_type = %s
        """, (username, doc_type))
    else:
        cur.execute("""
            SELECT filename FROM images 
            WHERE username = %s
        """, (username,))

    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return [{"filename": r[0]} for r in rows]
