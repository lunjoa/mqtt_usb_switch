import os
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


def toggle_ports(state):
    # Need to turn off both hub 1 and 3 on RPi 5, changes all ports. https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5
    hubcommand1 = f'uhubctl -l 1 -a {int(state)}'
    hubcommand2 = f'uhubctl -l 3 -a {int(state)}'
    hubcommands = {hubcommand1, hubcommand2}
    for hubcommand in hubcommands:
        run = os.popen(hubcommand)
        output = run.read()
        print(output)
        output = output.split("New status")[1]
        if state:
            if " off\n" in output or " power\n" not in output:
                raise UhubctlOutputError(hubcommand, output, "Should have resulted in Power for all ports")
        else:
            if " power\n" in output or " off\n" not in output:
                raise UhubctlOutputError(hubcommand, output, "Should have resulted in Off for all ports")


def ports_status():
    command = "uhubctl"
    output = os.popen(command).read()
    print(output)
    if " power\n" in output:
        toggle_ports(True)
        return "on"
    elif " off\n" in output:
        return "off"
    raise UhubctlOutputError(command, output)

# Callback function for when the client receives a CONNACK response from the server.
def on_connect(client, _userdata, _flags, rc, properties=None):
    print(f"Connected with result code {rc}.")
    # Subscribe to the control topic
    client.subscribe(TOPIC_SUBSCRIBE)
    client.publish(TOPIC_PUBLISH, ports_status())


# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == TOPIC_SUBSCRIBE:
        if msg.payload.decode() == "on":
            # Perform action to turn switch on
            toggle_ports(True)
            print("Switch turned on")
            client.publish(TOPIC_PUBLISH, "on")
        elif msg.payload.decode() == "off":
            # Perform action to turn switch off
            toggle_ports(False)
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
