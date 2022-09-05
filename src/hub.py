"""The controller hub script which connects to the MQTT broker and publishes the user's input to the 'LOCK' topic. It also subscribes to the 'LOCK_STATUS' topic
on the MQTT broker which is populated by the smart lock"""
import paho.mqtt.client as mqtt
import hashlib, os

from threading import Thread
from queue import Queue

class WakeUpHub:
    def __init__(self):
        self.file = "wake_word.txt"
        
    def check_wake_exists(self):
        if os.stat(self.file).st_size == 0:
            self.create_wake_word()
        else:
            return True
    
    def auth_wake_word(self, word):
        with open(self.file) as f:
            lines = f.readlines()
            if word == lines[0].strip():
                return True
            else:
                return False
    
    def create_wake_word(self):
        with open(self.file, "w") as f:
            wake_word = input ("Please create a custom wake word by entering it below\n>>>> ")
            f.write (wake_word)
            f.close()
    
    def wake_up(self):
        if os.stat(self.file).st_size == 0:
            self.create_wake_word()
            return self.wake_up()
        else:
            wake_word = input("Please enter wake word below:\n>>>>> ")
            return self.auth_wake_word(wake_word)

# Advises the user whether they are connected to the MQTT broker or not.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK_STATUS", qos=2)
    else:
        print("Failed to connect, return code %d\n", rc)

# Producer activity - reads the data from the MQTT server and puts it into the message queue to be processed by the consumer thread
def on_message(client, userdata, message):
    MsgQ.put(message.payload.decode())

def consumer():
    while True:
        msg = MsgQ.get()
        if msg == "Locked":
            print ("The door is locked")
        elif msg == "Unlocked":
            print ("The door is unlocked")
        else:
            print ("Unknown command recieved")
        MsgQ.task_done()

# Publishes the user's request to lock/unlock to the MQTT broker. If the input is invalid, it asks the user to enter a valid option or allows them to exit.
def user_action(user_input):
    if user_input.lower() == "lock":
        client.publish("LOCK", "Lock", qos=2) #Publishes 'Lock' to the MQTT broker topic 'LOCK'
    elif user_input.lower() == "unlock":
        client.publish("LOCK", "Unlock", qos=2)
    elif user_input.lower() == "exit":
        exit()
    else:
        print ("Please enter a valid option below\n>>>")
        action = input()
        user_action(action)

def broker_auth():
    with open("hub_passwordfile.txt") as f:
        lines = f.readlines()
        user = lines[0].strip()
        passwd = lines[1].strip()
    return user, passwd

def check_wake_exists():
    with open("wake_word.txt") as f:
        lines = f.readlines()
        if len.lines[0] == 0:
            wake_word = input("Please create a custom wake word by entering it below\n>>>> ")

# asks user for their input, calls the function to verify the user input
def user_interface():
    wake = WakeUpHub()
    if wake.wake_up() == True:
        print ("What would you like to do?\n-Unlock\n-Lock\n-Exit\nPlease type your request below\n>>>")
        action = input()
        user_action(action)
    else:
       print ("You do not have access")
       exit()

# Set up message queue
MsgQ = Queue()

# Start the consumer thread
t = Thread(target=consumer)
t.daemon = True
t.start()

# Identifying online broker location - Eclipse mosquito
#mqttBroker ="mqtt.eclipseprojects.io"
mqttBroker ="0.0.0.0"

# Setting up a new client and telling it to connect to the broker
client = mqtt.Client("Hub-984323")
client.username_pw_set(broker_auth()[0], broker_auth()[1])
client.connect(mqttBroker)

#client.on_connect = on_connect
user_interface()

client.on_connect = on_connect
client.on_message=on_message

client.loop_forever()
