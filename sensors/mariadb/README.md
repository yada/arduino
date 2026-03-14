# MariaDB – Sensor Metrics Storage

## Purpose

MariaDB is used to store sensor metrics (temperature, humidity, luminosity) read from the Arduino board via the serial port. The Python scripts (`serial-to-db.py`, `mariadb-test.py`) connect to this database to insert and query readings.

## Prerequisites

- MariaDB server installed and running
- Root access to create the database and user

## Database Setup

### 1. Create the database and user

```bash
mariadb -u root -p <<'SQL'
CREATE DATABASE IF NOT EXISTS arduino_db;
CREATE USER IF NOT EXISTS 'arduino'@'localhost' IDENTIFIED BY 'ChangeMeStrong!';
GRANT ALL PRIVILEGES ON arduino_db.* TO 'arduino'@'localhost';
FLUSH PRIVILEGES;
SQL
```

### 2. Create the sensors table

```bash
mariadb -u root -p arduino_db <<'SQL'
CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    luminosity INT NOT NULL CHECK (luminosity BETWEEN 0 AND 1023),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SQL
```

## Verify the setup

Connect as the `arduino` user and confirm the table exists:

```bash
mariadb -u arduino -p arduino_db -e "DESCRIBE sensors;"
```

## Test script

Run `mariadb-test.py` to insert a sample row and read it back:

```bash
python3 mariadb-test.py
```

