Toggle the VBUS (5V power) for the USB ports on a raspberry pi 5.
This script uses uhubctl https://github.com/mvp/uhubctl to do this. 


The script receives on/off commands over MQTT and publishes changed states. 
Designed for use with Home Assistant. Use case in mind: power down the display of 3D printer Creality Ender 3 when the printer is not in use. Combined with an IoT relay on the mains this keeps the printer fully off when not in use (no more noise or blue light).

# Requirements
Raspberry Pi 5, untested on any other hardware

# Providing permissions
The running user needs permission to control the usb controllers. Providing these is prefered, otherwise the script has to be run as root.
See https://github.com/mvp/uhubctl#linux-usb-permissions

Uhubctl provides these preconfigured udev rules: https://github.com/mvp/uhubctl/blob/master/udev/rules.d/52-usb.rules download them:
```
wget "https://raw.githubusercontent.com/mvp/uhubctl/master/udev/rules.d/52-usb.rules"
```

Change owner and move them into /etc/udev/rules.d/:
```
sudo chown root:root 52-usb.rules && sudo mv 52-usb.rules /etc/udev/rules.d/52-usb.rules
```

Add the current user to the dialout group to provide the required permissions. Change $USER if you need to give permissions to a user other than the current:
```
sudo usermod -a -G dialout $USER
```

For your udev rule changes to take effect, reboot or run:
```
sudo udevadm trigger --attr-match=subsystem=usb
```


# Using docker
If using docker, make sure the user running docker has permissions as per the instructions above.

Copy .env.example to .env:
```
cp .env.example .env
```
Edit .env to your parameters:
```
USB_SWITCH_EXIT_STATUS=on # The status to apply on program exit. Possible options: on, off, keep
MQTT_SERVER=host.domain # The domain name or IP of the broker host
MQTT_PORT=1883
USB_SWITCH_USER=user # MQTT username
USB_SWITCH_PASSWORD=password # MQTT password
```

Build docker image with name mqtt_usb_switch:
```
docker build -t mqtt_usb_switch .
```

Compose:
```
docker compose up -d
```
As in docker-compose.yaml, the container has to be run in host network mode to interact with the broker, not sure why. 
