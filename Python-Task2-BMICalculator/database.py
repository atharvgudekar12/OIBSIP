import sqlite3
from datetime import datetime


DATABASE_NAME = "data/bmi_history.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_record(user_name, weight, height, bmi, category):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO bmi_records
        (user_name, weight, height, bmi, category, date_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        weight,
        height,
        bmi,
        category,
        date_time
    ))

    connection.commit()
    connection.close()

def get_all_records():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_name, weight, height, bmi, category, date_time
        FROM bmi_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records