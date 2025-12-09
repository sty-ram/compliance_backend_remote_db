# import mysql.connector

# import mysql.connector
# from dotenv import load_dotenv
# import os

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_NAME = os.getenv("DB_NAME")

# def get_connection():
#     return mysql.connector.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME
#     )


# # ----------------------------
# # USER FUNCTIONS
# # ----------------------------

# def create_user(username, password_hash):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO users (username, password) 
#         VALUES (%s, %s)
#     """, (username, password_hash))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return {"status": "success"}


# def fetch_user(username):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
#     row = cur.fetchone()

#     cur.close()
#     conn.close()

#     if row:
#         return {"username": row[0], "password": row[1]}
#     return None


# # ----------------------------
# # IMAGE FUNCTIONS
# # ----------------------------

# def upload_image_to_db(username, file, doc_type):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO images (username, doc_type, filename, filedata)
#         VALUES (%s, %s, %s, %s)
#     """, (username, doc_type, file.filename, file.read()))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return {"status": "success"}


# def fetch_user_images(username, doc_type=None):
#     conn = get_connection()
#     cur = conn.cursor()

#     if doc_type:
#         cur.execute("""
#             SELECT filename FROM images 
#             WHERE username = %s AND doc_type = %s
#         """, (username, doc_type))
#     else:
#         cur.execute("""
#             SELECT filename FROM images 
#             WHERE username = %s
#         """, (username,))

#     rows = cur.fetchall()
    
#     cur.close()
#     conn.close()
    
#     return [{"filename": r[0]} for r in rows]


import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# -------------------------------------------------------------------
# DB CONNECTION
# -------------------------------------------------------------------
def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        print("DB CONNECTION ERROR:", str(e))
        raise Exception(f"Database connection failed: {str(e)}")


# -------------------------------------------------------------------
# USER FUNCTIONS
# -------------------------------------------------------------------
def create_user(username, password_hash):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}

    except mysql.connector.IntegrityError:
        return {"error": "Username exists", "code": 400}

    except Exception as e:
        print("CREATE USER ERROR:", str(e))
        return {"error": str(e), "code": 500}


def fetch_user(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result

    except Exception as e:
        print("FETCH USER ERROR:", str(e))
        return None


# -------------------------------------------------------------------
# IMAGE FUNCTIONS
# -------------------------------------------------------------------
def upload_image_to_db(username, file, doc_type):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO images (username, doc_type, filename, filedata)
            VALUES (%s, %s, %s, %s)
        """, (username, doc_type, file.filename, file.read()))

        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success"}

    except Exception as e:
        print("UPLOAD IMAGE ERROR:", str(e))
        return {"error": str(e), "code": 500}


def fetch_user_images(username, doc_type=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if doc_type:
            cursor.execute("""
                SELECT filename FROM images 
                WHERE username=%s AND doc_type=%s
            """, (username, doc_type))
        else:
            cursor.execute("""
                SELECT filename FROM images 
                WHERE username=%s
            """, (username,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [{"filename": r[0]} for r in rows]

    except Exception as e:
        print("FETCH IMAGES ERROR:", str(e))
        return []
