# Python Virtual Environment

## Purpose

This `venv` directory contains a Python 3.11 virtual environment used to isolate the dependencies needed by the sensor scripts (`serial-to-db.py`, `mariadb-test.py`, etc.).

## Installed packages

- **pyserial** — serial communication with the Arduino
- **mariadb** — Python connector to insert sensor data into MariaDB

## Recreating the environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyserial mariadb
```
