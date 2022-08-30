"""Subscriber of the smart lock topic"""
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("LOCK")

def on_message(client, userdata, message):
    if message.payload.decode() == "Lock":
        client.publish("LOCK_STATUS", "Locked")
        print ("Locked")
        client.disconnect()
    else:
        client.publish("LOCK_STATUS", "Unlocked")
        print ("Unlocked")
        client.disconnect()

# MQTT broker location online
mqttBroker ="mqtt.eclipseprojects.io"

#Setting up a new client to connect to the broker to subscribe to the temperature and connecting this client to the broker
client = mqtt.Client("Hub")
client.connect(mqttBroker)

#The topic in the MQTT broker to subscribe to
client.on_connect = on_connect
client.on_message=on_message

#loop
client.loop_forever()
