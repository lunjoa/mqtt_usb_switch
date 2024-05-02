import os
import paho.mqtt.client as mqtt

# MQTT Broker details
MQTT_SERVER = os.environ.get('MQTT_SERVER')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
USERNAME = os.environ.get('USB_SWITCH_USER')
PASSWORD = os.environ.get('USB_SWITCH_PASSWORD')

# MQTT topics
topic_subscribe = "usb_switch/set"
topic_publish = "usb_switch"

# Callback function for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to the control topic
    client.subscribe(topic_subscribe)

# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_subscribe:
        if msg.payload.decode() == "on":
            # Perform action to turn switch on
            os.system('uhubctl -l 1 -a 1')
            os.system('uhubctl -l 3 -a 1')
            print("Switch turned on")
            client.publish(topic_publish, "on")
        elif msg.payload.decode() == "off":
            # Perform action to turn switch off
            os.system('uhubctl -l 1 -a 0')
            os.system('uhubctl -l 3 -a 0')
            print("Switch turned off")
            client.publish(topic_publish, "off")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.username_pw_set(USERNAME, PASSWORD)  # Set username and password if required
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Loop to stay connected and process messages
client.loop_forever()
