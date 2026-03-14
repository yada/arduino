#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Reception des données émise par un Arduino branché
à un port USB.

'''

import serial                    # pyserial: communicate with the Arduino over USB
import serial.tools.list_ports   # helper to discover available serial ports

# Step 1: Scan for all available serial ports on the machine
print("Recherche d'un port serie...")

ports = serial.tools.list_ports.comports(include_links=False)

if (len(ports) != 0): # at least one active port was found

    # Step 2: Display how many ports were detected
    if (len(ports) > 1):
        print (str(len(ports)) + " ports actifs ont ete trouves:") 
    else:
        print ("1 port actif a ete trouve:")

    # List each port with a number so the user can pick one
    ligne = 1

    for port in ports :
        print(str(ligne) + ' : ' + port.device)  # e.g. "1 : /dev/ttyACM0"
        ligne = ligne + 1

    # Step 3: Ask the user which port the Arduino is connected to
    portChoisi = int(input('Ecrivez le numero du port desire:'))

    # Step 4: Ask the user to choose a baud rate
    # The baud rate must match the value set in the Arduino sketch (Serial.begin)
    print('1: 9600   2: 38400    3: 115200')

    baud = int(input('Ecrivez le baud rate desire:'))

    # Map the user's menu choice (1, 2, 3) to the actual baud rate value
    if (baud == 1):
        baud = 9600
    if (baud == 2):
        baud = 38400
    if (baud == 3):
        baud = 115200

    # Step 5: Open the serial connection to the Arduino
    # timeout=1 means readline() will wait up to 1 second for data
    arduino = serial.Serial(ports[portChoisi - 1].device, baud, timeout=1)
    
    print('Connexion a ' + arduino.name + ' a un baud rate de ' + str(baud))

    # Step 6: Continuously read and display data from the Arduino
    # Each line sent by Serial.println() on the Arduino is read here
    while True:
        data = arduino.readline().decode('utf-8').strip()  # read one line and decode bytes to string
        if data:
            print (data)  # print only non-empty lines

else: # no active serial port was found — is the Arduino plugged in?
    print("Aucun port actif n'a ete trouve")
