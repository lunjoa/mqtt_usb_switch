FROM python:3.12-bookworm

# Have to compile uhubctl from source, there is no release with support for RPi5
# See https://github.com/mvp/uhubctl?tab=readme-ov-file#compiling
RUN apt-get update && apt-get install -y libusb-1.0-0-dev

RUN git clone https://github.com/mvp/uhubctl

RUN make -C uhubctl

RUN make -C uhubctl install


COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY mqtt_usb_switch.py .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "./mqtt_usb_switch.py"]
