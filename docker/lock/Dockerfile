# Dockerfile, Image, Container

FROM python:3.10.6

LABEL description="MQTT LOCK v0.01"

ADD lock.py lock_passwordfile.txt ./

RUN pip install paho-mqtt

CMD ["python", "./lock.py"]
