import paho.mqtt.client as mqtt
import time
import sys
import threading
import atexit
import signal

# MQTT Configuration
broker_address = "broker.emqx.io"
broker_port = 1883
topic = "/student_group/light_control/drefault"
heartbeat_topic = "/student_group/device_heartbeat/drefault"
status_topic = "/student_group/device_status/drefault"
client_id = "python_iot_simulator"
light_state = "OFF"
class Colors:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{Colors.GREEN}Connected to MQTT Broker!{Colors.ENDC}")
        
        # Clear any retained messages
        client.publish(topic, '', retain=True)
        time.sleep(0.1)  # Small delay to ensure the message is processed
        
        # Now subscribe to the topic
        client.subscribe(topic)
        print(f"{Colors.BLUE}Subscribed to topic: {topic}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Waiting for commands...{Colors.ENDC}")
      
        client.publish(status_topic, f"READY:{light_state}", qos=1, retain=True)
    else:
        print(f"{Colors.RED}Failed to connect, return code {rc}{Colors.ENDC}")

def on_message(client, userdata, msg):
    global light_state
    message = msg.payload.decode()
    print(f"\nReceived message on topic {msg.topic}: {message}")
    
    if message == "ON":
        light_state = "ON"
        print(f"{Colors.YELLOW}💡 Light is TURNED ON{Colors.ENDC}")
        # Send status update
        client.publish(status_topic, "STATE:ON", qos=1)
    elif message == "OFF":
        light_state = "OFF"
        print(f"{Colors.BLUE}💡 Light is TURNED OFF{Colors.ENDC}")
        # Send status update
        client.publish(status_topic, "STATE:OFF", qos=1)
    else:
        print(f"{Colors.RED}Unknown command: {message}{Colors.ENDC}")

# Function to send heartbeat messages
def send_heartbeats(client):
    while True:
        try:
            client.publish(heartbeat_topic, "alive", qos=1)
            time.sleep(5)  # Send heartbeat every 5 seconds
        except Exception as e:
            print(f"{Colors.RED}Error sending heartbeat: {e}{Colors.ENDC}")
            break

# Function to handle clean shutdown
def shutdown_handler():
    print(f"\n{Colors.YELLOW}Sending shutdown notification...{Colors.ENDC}")
    try:
        # Send shutdown message with retain flag to persist the message
        client.publish(status_topic, "SHUTDOWN", qos=1, retain=True)
        time.sleep(0.5)  # Give time for the message to be sent
        
        client.disconnect()
        print(f"{Colors.GREEN}Disconnected. Goodbye!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Error during shutdown: {e}{Colors.ENDC}")
atexit.register(shutdown_handler)

def signal_handler(sig, frame):
    print(f"\n{Colors.RED}Received termination signal. Shutting down...{Colors.ENDC}")
    sys.exit(0) 

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
print(f"Connecting to MQTT broker at {broker_address}:{broker_port}...")
try:
    client.connect(broker_address, broker_port, 60)
    
    # Start heartbeat thread to monitorconnection
    heartbeat_thread = threading.Thread(target=send_heartbeats, args=(client,))
    heartbeat_thread.daemon = True 
    heartbeat_thread.start()
    
except Exception as e:
    print(f"{Colors.RED}Failed to connect to broker: {e}{Colors.ENDC}")
    sys.exit(1)
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass 