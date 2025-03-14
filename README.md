# MQTT-Based Light Control

This project demonstrates a simple IoT application that controls a virtual light using MQTT protocol. It consists of a web interface for controlling the light and a Python script that simulates an IoT device (like an ESP8266).

## Components

1. **Web Interface (index.html)**
   - Simple UI with ON/OFF buttons
   - Uses MQTT.js to publish commands over WebSockets
   - Shows the current status of the light

2. **IoT Device Simulator (light_simulation.py)**
   - Python script that simulates an ESP8266 device
   - Subscribes to MQTT topic and listens for commands
   - Displays the light status in the console

## How to Use

### Setup and Run the IoT Device Simulator

1. Make sure you have Python installed
2. Install the required package:
   ```
   pip install paho-mqtt
   ```
3. Run the simulator:
   ```
   python light_simulation.py
   ```

### Use the Web Interface

1. Open `index.html` in a web browser
2. The page will automatically connect to the MQTT broker
3. Click the "Turn ON" or "Turn OFF" button to control the light
4. The simulator will display the current state of the light

## MQTT Details

- Broker: broker.emqx.io
- Port: 1883 (TCP) / 8084 (WebSocket)
- Topic: /student_group/light_control
- Messages: "ON" or "OFF"

## Technologies Used

- HTML, CSS, JavaScript
- MQTT.js for browser-based MQTT communication
- Paho MQTT for Python
- EMQX as the public MQTT broker

## Notes

This is a simulation only. In a real-world scenario, the Python script would be replaced with actual code running on an ESP8266 or similar microcontroller, which would control a physical light or relay.
