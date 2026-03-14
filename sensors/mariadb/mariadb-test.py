#!/usr/bin/env python3
import mariadb
import sys

db_config = {
    "user": "arduino",
    "password": "ChangeMeStrong!",
    "host": "127.0.0.1",
    "database": "arduino_db",
    "port": 3306,
}

try:
    conn = mariadb.connect(**db_config)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}", file=sys.stderr)
    sys.exit(1)

cur = conn.cursor()

# Insert test data
cur.execute(
    "INSERT INTO sensors (temperature, humidity, luminosity) VALUES (?, ?, ?)",
    (22.5, 45.3, 512),
)
conn.commit()

# Read data
cur.execute("SELECT * FROM sensors")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
