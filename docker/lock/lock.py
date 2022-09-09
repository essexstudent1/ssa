"""The smart lock script which subscribes to the MQTT broker 'LOCK' topic, triggers the doors to be locked and then publishes to the topic 'LOCK_STATUS' on the
MQTT broker"""
import paho.mqtt.client as mqtt

from threading import Thread
from queue import Queue


# Define the Smartlock class
class SmartLock:
    def __init__(self):
        # insert code here to interface with hardware and read the initial status of the lock.
        # since we don't have real hardware, we are going to assume that the lock always initializes to unlocked
        self.status = 0

    def lock(self):
        # insert code here to interface with hardware and secure the lock
        # ideally we would have error handling here in case the lock fails to secure. we are assuming the locking mechanism always works.
        self.status = 1  # status = 1 = locked
        client.publish("LOCK_STATUS", "Locked", qos=2)
        print("The door is locked")

    def unlock(self):
        # insert code here to interface with hardware and open the lock
        # ideally we would have error handling here in case the lock fails to open. we are assuming the unlocking mechanism always works.
        self.status = 0  # status = 0 = unlocked
        client.publish("LOCK_STATUS", "Unlocked", qos=2)
        print("The door is unlocked")


# Pulls the broker login details from a password file
def broker_auth():
    with open("lock_passwordfile.txt") as f:
        lines = f.readlines()
        user = lines[0].strip()
        passwd = lines[1].strip()
    return user, passwd


# Advises the user whether they are connected to the MQTT broker or not.
def on_connect(client, userdata, flags, r_c):
    if r_c == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK", qos=2)
    else:
        print("Failed to connect, return code %d\n", r_c)


# Producer activity - reads the data from the MQTT server and puts it into the message queue to be processed by the consumer thread
def on_message(client, userdata, message):
    MsgQ.put(message.payload.decode())


# Define the consumer thread to read the message queue and call the appropriate smartlock function
def consumer():
    while True:
        msg = MsgQ.get()
        if msg == "Lock":
            MyLock.lock()
        elif msg == "Unlock":
            MyLock.unlock()
        else:
            print("Unknown command recieved")
        MsgQ.task_done()


# Initialize the lock
MyLock = SmartLock()

# Set up message queue
MsgQ = Queue()

# Start the consumer thread
t = Thread(target=consumer)
t.daemon = True
t.start()

# MQTT broker location, currently set to localhost
MQTT_BROKER = "mqtt.aliahmed.app"

# Setting up a new client to connect to the broker to subscribe to the lock status and connecting this client to the broker
client = mqtt.Client("Lock-984323")
client.username_pw_set(broker_auth()[0], broker_auth()[1])
client.connect(MQTT_BROKER)

# The topic in the MQTT broker to subscribe to
client.on_connect = on_connect
client.on_message = on_message

# Producer thread loops continually looking for messages from the MQTT server
client.loop_forever()
