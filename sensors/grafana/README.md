# Grafana – Sensor Dashboard

## Purpose

Grafana is used to visualize sensor metrics (temperature, humidity, luminosity)
stored in MariaDB. The exported JSON dashboard can be imported into any fresh
Grafana installation to get the same panels and layout.

## Install Grafana on Raspberry Pi

sudo apt-get install gnupg2

Full guide: https://grafana.com/tutorials/install-grafana-on-raspberry-pi/

## Configure the MariaDB data source

1. Open Grafana (default: http://localhost:3000)
2. Go to Connections > Data sources > Add data source
3. Choose MySQL
4. Fill in the connection details:
   - Host: 127.0.0.1:3306
   - Database: arduino_db
   - User: arduino
   - Password: (your password)
5. Click "Save & test"

## Import the dashboard

1. Go to Dashboards > New > Import
2. Click "Upload dashboard JSON file"
3. Select: Arduino-Sensors-1773511729161.json
4. Choose the MariaDB data source you just created
5. Click "Import"

The dashboard shows temperature, humidity and luminosity panels
with data collected every 2 minutes from the Arduino sensors.

