# Dockerfile, Image, Container

FROM python:3.10.6

LABEL description="MQTT HUB v0.01"

COPY hub.py hub_passwordfile.txt wake_word.txt filekey.key ./

RUN pip install paho-mqtt cryptography pydal

CMD ["python", "./hub.py"]
