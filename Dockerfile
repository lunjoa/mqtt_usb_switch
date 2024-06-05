FROM python:3.12-slim

RUN apt-get update && apt-get install -y uhubctl

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY mqtt_usb_switch.py .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "./mqtt_usb_switch.py"]
