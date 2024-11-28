import sqlite3
from datetime import datetime

DB_NAME = "cars.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id TEXT UNIQUE,
            title TEXT,
            price TEXT,
            mileage TEXT,
            location TEXT,
            link TEXT,
            photos TEXT,
            last_seen TIMESTAMP,
            message_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_existing_car(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE link = ?", (link,))
    result = cursor.fetchone()
    conn.close()
    return result

def add_or_update_car(car,existing=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now()

    if existing:
        cursor.execute("""
            UPDATE cars
            SET price = ?, last_seen = ?
            WHERE link = ?
        """, (car["price"], now, car["link"]))
    else:
        # Insert new car
        cursor.execute("""
            INSERT INTO cars (car_id, title, price, mileage, location, link, photos, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            car["link"].split("/")[-1].split(".")[0],
            car["title"], car["price"], car["mileage"],
            car["location"], car["link"],
            ",".join(car["photos"]), now
        ))
    conn.commit()
    conn.close()

def get_all_cars():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    results = cursor.fetchall()
    conn.close()
    return results

def get_active_car_links():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM cars")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def save_message_id(link, message_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE cars SET message_id = ? WHERE link = ?", (message_id, link))
    conn.commit()
    conn.close()