#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read Arduino CSV lines: temperature,humidity,luminosity
Example: 17.10,44.00,43
Insert into MariaDB table: sensors(temperature, humidity, luminosity)
"""

from __future__ import annotations

import sys
import serial
import serial.tools.list_ports
import mariadb

DB_CONFIG = {
    "user": "arduino",
    "password": "ChangeMeStrong!",
    "host": "127.0.0.1",
    "database": "arduino_db",
    "port": 3306,
    "connect_timeout": 5,
}

BAUD_RATE = 9600


def choose_port(ports) -> str:
    print("\nAvailable serial ports:")
    for i, p in enumerate(ports, start=1):
        extra = f" — {p.description}" if p.description else ""
        print(f"{i}: {p.device}{extra}")

    while True:
        choice = input("Enter the port number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(ports):
            return ports[int(choice) - 1].device
        print(f"Please choose a number between 1 and {len(ports)}.")


def parse_csv_line(line: str) -> tuple[float, float, int] | None:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 3:
        return None
    try:
        temperature = float(parts[0])
        humidity = float(parts[1])
        luminosity = int(parts[2])
    except ValueError:
        return None

    if not (0 <= luminosity <= 1023):
        return None

    return temperature, humidity, luminosity


def main() -> int:
    ports = list(serial.tools.list_ports.comports(include_links=False))
    if not ports:
        print("No active serial ports found.")
        return 1

    port_device = choose_port(ports)

    try:
        conn = mariadb.connect(**DB_CONFIG)
    except mariadb.Error as e:
        print(f"MariaDB connection error: {e}", file=sys.stderr)
        return 2

    cur = conn.cursor()

    print(f"\nConnecting to {port_device} at {BAUD_RATE} baud...")
    try:
        with serial.Serial(port_device, BAUD_RATE, timeout=5) as arduino:
            print("Connected. Waiting for CSV lines... (Ctrl+C to stop)\n")

            while True:
                line = arduino.readline().decode("utf-8", errors="replace").strip()
                if not line:
                    continue

                parsed = parse_csv_line(line)
                if not parsed:
                    print(f"Skipping unrecognized line: {line}", file=sys.stderr)
                    continue

                temperature, humidity, luminosity = parsed

                cur.execute(
                    "INSERT INTO sensors (temperature, humidity, luminosity) VALUES (?, ?, ?)",
                    (temperature, humidity, luminosity),
                )
                conn.commit()

                print(f"Inserted: {temperature:.2f}°C, {humidity:.2f}%, {luminosity}")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}", file=sys.stderr)
        return 3
    except mariadb.Error as e:
        print(f"MariaDB error: {e}", file=sys.stderr)
        return 4
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
