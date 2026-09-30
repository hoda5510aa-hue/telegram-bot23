import os
import sqlite3

OWNER_ID = 8883976843
DB = os.getenv("DB_PATH", "users.db")


def connect():
    return sqlite3.connect(DB)



def setup():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        diamonds INTEGER DEFAULT 1000
    )
    """)

    conn.commit()
    conn.close()



def add_user(user_id, username):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username, diamonds)
        VALUES(?,?,1000)
        """,
        (
            user_id,
            username
        )
    )

    conn.commit()
    conn.close()



def get_balance(user_id):

    if user_id == OWNER_ID:
        return 999999999


    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT diamonds FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0

def change_diamonds(user_id, amount):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET diamonds = diamonds + ?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()
    conn.close()



def set_diamonds(user_id, amount):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET diamonds=?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()
    conn.close()



def user_exists(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    conn.close()

    return result is not None


