Toggle the VBUS (5V power) for the USB ports on a raspberry pi 5.
This script uses uhubctl https://github.com/mvp/uhubctl to do this. 
See https://github.com/mvp/uhubctl#linux-usb-permissions and https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5

Make sure the version of uhubctl you are using works properly with RPi 5 if that's the use case.

The script receives on/off commands over MQTT and publishes changed states. 
Designed for use with Home Assistant.
