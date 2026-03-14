#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read Arduino CSV lines: temperature,humidity,luminosity
Example: 17.10,44.00,43
Insert into MariaDB table: sensors(temperature, humidity, luminosity)
"""

from __future__ import annotations

import sys
import serial                    # pyserial: communicates with the Arduino over USB
import serial.tools.list_ports   # helper to discover available serial ports
import mariadb                   # Python connector for MariaDB database

# Database connection settings — must match what was created in mariadb/README.md
DB_CONFIG = {
    "user": "arduino",
    "password": "ChangeMeStrong!",
    "host": "127.0.0.1",        # localhost (the DB runs on the same Raspberry Pi)
    "database": "arduino_db",
    "port": 3306,                # default MariaDB port
    "connect_timeout": 5,
}

# Baud rate must match the value in sensors.ino: Serial.begin(9600)
BAUD_RATE = 9600


def choose_port(ports) -> str:
    """Display all detected serial ports and let the user pick one.
    The Arduino typically shows up as /dev/ttyACM0 on Linux/Raspberry Pi."""
    print("\nAvailable serial ports:")
    for i, p in enumerate(ports, start=1):
        extra = f" — {p.description}" if p.description else ""
        print(f"{i}: {p.device}{extra}")

    # Keep asking until the user enters a valid number
    while True:
        choice = input("Enter the port number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(ports):
            return ports[int(choice) - 1].device
        print(f"Please choose a number between 1 and {len(ports)}.")


def parse_csv_line(line: str) -> tuple[float, float, int] | None:
    """Parse a CSV line sent by the Arduino, e.g. '17.10,44.00,43'.
    Returns a (temperature, humidity, luminosity) tuple, or None if invalid."""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 3:
        return None  # we expect exactly 3 comma-separated values
    try:
        temperature = float(parts[0])   # degrees Celsius
        humidity = float(parts[1])      # percentage
        luminosity = int(parts[2])      # analog reading 0–1023
    except ValueError:
        return None  # not a number — probably a debug message from the Arduino

    # The analog pin returns values between 0 and 1023; reject anything outside
    if not (0 <= luminosity <= 1023):
        return None

    return temperature, humidity, luminosity


def main() -> int:
    # Step 1: Detect available serial ports (USB devices)
    ports = list(serial.tools.list_ports.comports(include_links=False))
    if not ports:
        print("No active serial ports found.")
        return 1

    port_device = choose_port(ports)

    # Step 2: Connect to MariaDB so we can store the readings
    try:
        conn = mariadb.connect(**DB_CONFIG)
    except mariadb.Error as e:
        print(f"MariaDB connection error: {e}", file=sys.stderr)
        return 2

    cur = conn.cursor()  # a cursor lets us execute SQL queries

    # Step 3: Open the serial connection and read data in a loop
    print(f"\nConnecting to {port_device} at {BAUD_RATE} baud...")
    try:
        with serial.Serial(port_device, BAUD_RATE, timeout=5) as arduino:
            print("Connected. Waiting for CSV lines... (Ctrl+C to stop)\n")

            while True:
                # Read one line from the Arduino (blocks until a newline arrives)
                line = arduino.readline().decode("utf-8", errors="replace").strip()
                if not line:
                    continue  # empty line or timeout — try again

                # Try to parse the CSV line into numeric values
                parsed = parse_csv_line(line)
                if not parsed:
                    print(f"Skipping unrecognized line: {line}", file=sys.stderr)
                    continue

                temperature, humidity, luminosity = parsed

                # Insert the reading into the 'sensors' table
                # The '?' placeholders prevent SQL injection
                cur.execute(
                    "INSERT INTO sensors (temperature, humidity, luminosity) VALUES (?, ?, ?)",
                    (temperature, humidity, luminosity),
                )
                conn.commit()  # save the row to the database immediately

                print(f"Inserted: {temperature:.2f}°C, {humidity:.2f}%, {luminosity}")

    except KeyboardInterrupt:
        print("\nStopped by user.")  # user pressed Ctrl+C
    except serial.SerialException as e:
        print(f"Serial error: {e}", file=sys.stderr)  # USB cable disconnected?
        return 3
    except mariadb.Error as e:
        print(f"MariaDB error: {e}", file=sys.stderr)  # database went away?
        return 4
    finally:
        # Always close the database connection when done, even if an error occurred
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

    return 0  # success


if __name__ == "__main__":
    raise SystemExit(main())
