"""The smart lock script which subscribes to the MQTT broker 'LOCK' topic, triggers the doors to be locked and then publishes to the topic 'LOCK_STATUS' on the
MQTT broker"""
from threading import Thread
from queue import Queue
from datetime import datetime
import random
import paho.mqtt.client as mqtt

# Define the Smartlock class
class SmartLock:
    """smart lock class, lock or unlock option"""
    def __init__(self):
        # insert code here to interface with hardware and read the initial status of the lock.
        # assuming that the lock always initializes to unlocked
        self.status = 0

    def lock(self):
        """interact with hardware and secure the lock"""
        self.status = 1  # status = 1 = locked
        client.publish("LOCK_STATUS", "Locked", qos=2)
        print("The door is locked")

    def unlock(self):
        """insert code here to interact with hardware and open the lock"""
        self.status = 0  # status = 0 = unlocked
        client.publish("LOCK_STATUS", "Unlocked", qos=2)
        print("The door is unlocked")


def broker_auth():
    """Pulls the broker login details from a password file"""
    with open("lock_passwordfile.txt") as f:
        lines = f.readlines()
        user = lines[0].strip()
        passwd = lines[1].strip()
    return user, passwd


def on_connect(client, userdata, flags, r_c):
    """ Advises the user whether they are connected to the MQTT broker or not"""
    if r_c == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK", qos=2)
    else:
        print("Failed to connect, return code %d\n", r_c)



def on_message(client, userdata, message):
    """ Reads data from the MQTT server and puts into message queue to be processed"""
    MsgQ.put(message.payload.decode())



def consumer():
    """Consumer thread to read the message queue and call the appropriate smartlock function"""
    while True:
        msg = MsgQ.get()
        if msg == "Lock":
            MyLock.lock()
        elif msg == "Unlock":
            MyLock.unlock()
        else:
            print("Unknown command received")
        MsgQ.task_done()


def unique_number():
    """Generates a unique number using current date/time and random number"""
    n1 = datetime.now()
    return n1.strftime("%Y%m%d%H%M%S") + str(random.randint(0,9999))

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

# New client to connect to the broker to subscribe to the lock status
client = mqtt.Client("Lock-984323" + unique_number())
client.username_pw_set(broker_auth()[0], broker_auth()[1])
client.connect(MQTT_BROKER)

# The topic in the MQTT broker to subscribe to
client.on_connect = on_connect
client.on_message = on_message

# Producer thread loops continually looking for messages from the MQTT server
client.loop_forever()
