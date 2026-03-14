# Serial – Python Serial Demo

## Purpose

This is a simple demonstration of how to read serial data from an Arduino board using Python and the `pyserial` library. It is not meant for production use — just a quick way to verify that serial communication works.

## Script: `python-serial-from-arduino.py`

The script:

1. Lists all available serial ports
2. Lets you pick which port the Arduino is connected to
3. Lets you choose a baud rate (9600, 38400, or 115200)
4. Opens the serial connection and prints incoming data line by line

## Usage

```bash
python3 python-serial-from-arduino.py
```

### Requirements

```bash
pip install pyserial
```
