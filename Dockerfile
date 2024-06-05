FROM python:3.11.2

RUN apt-get update && apt-get install -y uhubctl

ADD requirements.txt .

ADD mqtt_usb_switch.py .

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./mqtt_usb_switch.py"]