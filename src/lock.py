"""The smart lock script which subscribes to the MQTT broker 'LOCK' topic, triggers the doors to be locked and then publishes to the topic 'LOCK_STATUS' on the 
MQTT broker"""
import paho.mqtt.client as mqtt

# Advises the user whether they are connected to the MQTT broker or not.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK")
    else:
        print("Failed to connect, return code %d\n", rc)

# Locks the door when it receives a command from the LOCK topic on the MQTT broker to which the controller hub publishes
# and sends the response back to the 'LOCK_STATUS' topic on the MQTT broker
def on_message(client, userdata, message):
    if message.payload.decode() == "Lock":
        client.publish("LOCK_STATUS", "Locked")
        print ("The door is locked")
    else:
        client.publish("LOCK_STATUS", "Unlocked")
        print ("The door is unlocked")

# MQTT broker location online
mqttBroker ="mqtt.eclipseprojects.io"

#Setting up a new client to connect to the broker to subscribe to the temperature and connecting this client to the broker
client = mqtt.Client("Hub")
client.connect(mqttBroker)

#The topic in the MQTT broker to subscribe to
client.on_connect = on_connect
client.on_message=on_message

client.loop_forever()