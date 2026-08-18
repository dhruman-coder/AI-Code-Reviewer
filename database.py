import sqlite3
from datetime import datetime


DATABASE = "reviews.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            language TEXT,
            score INTEGER,
            bugs INTEGER,
            security INTEGER,
            performance INTEGER,
            quality INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_review(
    language,
    score,
    bugs,
    security,
    performance,
    quality
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reviews
        (date, language, score, bugs, security, performance, quality)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        language,
        score,
        bugs,
        security,
        performance,
        quality
    ))

    connection.commit()
    connection.close()


def get_reviews():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            language,
            score,
            bugs,
            security,
            performance,
            quality
        FROM reviews
        ORDER BY id DESC
    """)

    reviews = cursor.fetchall()

    connection.close()

    return reviews