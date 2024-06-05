Toggle the VBUS (5V power) for the USB ports on a raspberry pi 5.
This script uses uhubctl https://github.com/mvp/uhubctl to do this. 
See https://github.com/mvp/uhubctl#linux-usb-permissions and https://github.com/mvp/uhubctl?tab=readme-ov-file#raspberry-pi-5

If using docker, make sure the user running docker has permissions as per the link above. Also make sure to create a .env file and specify the environment variables required, there is a provided .env.example. The container had to be run in host network mode to interact with the broker, not sure why. 

The script receives on/off commands over MQTT and publishes changed states. 
Designed for use with Home Assistant. Main use case being to power down the display of 3D printer Creality Ender 3 when the printer is not in use. Combined with an IoT relay on the mains this keeps the printer fully off when not in use (no more noise or blue light).
