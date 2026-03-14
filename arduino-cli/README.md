# Arduino CLI

## Purpose

The Arduino CLI allows compiling and uploading sketches to an Arduino board directly from the command line, without needing the Arduino IDE. This is especially useful when working on a Raspberry Pi or any headless environment.

## Usage

### Compile a sketch

```bash
./arduino-cli compile --fqbn arduino:avr:mega sensors.ino
```

### Upload a sketch to the board

```bash
./arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega sensors.ino
```

- `--fqbn arduino:avr:mega` — specifies the board type (Arduino Mega)
- `-p /dev/ttyACM0` — specifies the serial port the board is connected to
