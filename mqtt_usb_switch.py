import os
import paho.mqtt.client as mqtt


# MQTT topics
TOPIC_SUBSCRIBE = "usb_switch/set"
TOPIC_PUBLISH = "usb_switch"


def turn_on_ports():
    # Need to turn on both hub 1 and 3 on RPi 5, changes all ports. https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5
    os.popen('uhubctl -l 1 -a 1')
    os.popen('uhubctl -l 3 -a 1')


def turn_off_ports():
    # Need to turn off both hub 1 and 3 on RPi 5, changes all ports. https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5
    os.popen('uhubctl -l 1 -a 0')
    os.popen('uhubctl -l 3 -a 0')


# Callback function for when the client receives a CONNACK response from the server.
def on_connect(client, _userdata, _flags, rc, properties=None):
    print(f"Connected with result code {rc}.")
    # Subscribe to the control topic
    client.subscribe(TOPIC_SUBSCRIBE)


# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == TOPIC_SUBSCRIBE:
        if msg.payload.decode() == "on":
            # Perform action to turn switch on
            turn_on_ports()
            print("Switch turned on")
            client.publish(TOPIC_PUBLISH, "on")
        elif msg.payload.decode() == "off":
            # Perform action to turn switch off
            turn_off_ports()
            print("Switch turned off")
            client.publish(TOPIC_PUBLISH, "off")


def main():
    # MQTT Broker details
    MQTT_SERVER = os.getenv('MQTT_SERVER')
    MQTT_PORT = int(os.getenv('MQTT_PORT'))
    USER = os.getenv('USB_SWITCH_USER')
    PASSWORD = os.getenv('USB_SWITCH_PASSWORD')

    # Initialize MQTT client
    print(f"Connecting to MQTT broker at {MQTT_SERVER}:{MQTT_PORT} with user {USER}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT Broker
    client.username_pw_set(USER, PASSWORD)  # Set USER and password if required
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    # Loop to stay connected and process messages
    client.loop_forever()


if __name__ == "__main__":
    main()
