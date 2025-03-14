import paho.mqtt.client as mqtt
import time
import sys

# MQTT Configuration
broker_address = "broker.emqx.io"
broker_port = 1883
topic = "/student_group/light_control"
client_id = "python_iot_simulator"

# Terminal colors for better visualization
class Colors:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{Colors.GREEN}Connected to MQTT Broker!{Colors.ENDC}")
        # Subscribe to the topic
        client.subscribe(topic)
        print(f"{Colors.BLUE}Subscribed to topic: {topic}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Waiting for commands...{Colors.ENDC}")
    else:
        print(f"{Colors.RED}Failed to connect, return code {rc}{Colors.ENDC}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"\nReceived message on topic {msg.topic}: {message}")
    
    if message == "ON":
        print(f"{Colors.YELLOW}💡 Light is TURNED ON{Colors.ENDC}")
    elif message == "OFF":
        print(f"{Colors.BLUE}💡 Light is TURNED OFF{Colors.ENDC}")
    else:
        print(f"{Colors.RED}Unknown command: {message}{Colors.ENDC}")

# Create MQTT client instance
client = mqtt.Client(client_id)

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
print(f"Connecting to MQTT broker at {broker_address}:{broker_port}...")
try:
    client.connect(broker_address, broker_port, 60)
except Exception as e:
    print(f"{Colors.RED}Failed to connect to broker: {e}{Colors.ENDC}")
    sys.exit(1)

# Start the loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    print(f"\n{Colors.RED}Disconnecting from broker...{Colors.ENDC}")
    client.disconnect()
    print(f"{Colors.GREEN}Disconnected. Goodbye!{Colors.ENDC}") 