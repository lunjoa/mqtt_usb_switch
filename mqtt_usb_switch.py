import atexit
import os
import subprocess
import paho.mqtt.client as mqtt


# MQTT topics
TOPIC_SUBSCRIBE = "usb_switch/set"
TOPIC_PUBLISH = "usb_switch"

class UhubctlOutputError(Exception):
    def __init__(self, command, output, message="Unexpected output from uhubctl"):
        self.command = command
        self.output = output
        self.message = message
        super().__init__(f"{message}: '{command}' output was '{output}'")


def set_ports(state):
    # Need to turn off both hub 1 and 3 on RPi 5, changes all ports. https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5
    for hubcommand in {f'uhubctl -l 1 -a {int(state)}', f'uhubctl -l 3 -a {int(state)}'}:
        try:
            output = subprocess.run(hubcommand, capture_output=True, encoding="utf-8", shell=True, check=True)
            print(output.stdout)
        except subprocess.CalledProcessError as e:
            raise UhubctlOutputError(hubcommand, e.stderr) from e


def ports_status():
    command = "uhubctl"
    try:
        output = subprocess.run(command, capture_output=True, encoding="utf-8", shell=True, check=True)
        print(output.stdout)
        return "power" in output.stdout
    except subprocess.CalledProcessError as e:
        raise UhubctlOutputError(command, e.stderr) from e


# Callback function for when the client receives a CONNACK response from the server.
def on_connect(client, _userdata, _flags, rc, properties=None):
    print(f"Connected with result code {rc}.")
    # Subscribe to the control topic
    client.subscribe(TOPIC_SUBSCRIBE)
    status = ports_status()
    set_ports(status)
    client.publish(TOPIC_PUBLISH, "on" if status else "off")


# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == TOPIC_SUBSCRIBE:
        if msg.payload.decode() == "on":
            # Perform action to turn switch on
            set_ports(True)
            print("Switch turned on")
            client.publish(TOPIC_PUBLISH, "on")
        elif msg.payload.decode() == "off":
            # Perform action to turn switch off
            set_ports(False)
            print("Switch turned off")
            client.publish(TOPIC_PUBLISH, "off")

def exit_handler(status):
    print(f"Terminating, following user preference USB_SWITCH_EXIT_STATUS: \"{status}\"")
    if status == "on":
        print("Making sure to power on USB-ports:")
        set_ports(True)
    elif status == "off":
        print("Making sure to power off USB-ports:")
        set_ports(False)
    elif status == "keep":
        print("Keeping current USB-ports status:")
        ports_status()
    else:
        print(f"Unrecognized USB_SWITCH_EXIT_STATUS: \"{status}\"")
        print("Keeping current USB-ports status:")
        ports_status()

def main():
    # Exit status user preference
    EXIT_STATUS = os.getenv("USB_SWITCH_EXIT_STATUS")
    atexit.register(exit_handler, EXIT_STATUS)

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
