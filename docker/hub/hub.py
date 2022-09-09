"""The controller hub script which connects to the MQTT broker and publishes
the user's input to the 'LOCK' topic. It also subscribes to the 'LOCK_STATUS'
topic on the MQTT broker which is populated by the smart lock"""
import time
import os
import sys
from threading import Thread
from queue import Queue
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt


class Encryption:
    """Define the encryption class to encrypt and decrypt the hub
    wakeup password"""
    def __init__(self):
        self.file = "wake_word.txt"
        self.key_file = "filekey.key"

    def generate_key(self):
        """Generates an encryption key and stores it in a file"""
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as filekey:
            filekey.write(key)

    def encrypt_wake_word(self):
        """Encrypts the wake word entered by using the encryption key from
        the file, stores the encrypted wake word in a file"""
        with open(self.key_file, "rb") as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open(self.file, "rb") as file:
            original_file = file.read()
        encrypted = fernet.encrypt(original_file)
        with open(self.file, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypt_wake_word(self):
        """Decrypts the wake word entered by the user using the encryption key
        from the file"""
        with open(self.key_file, "rb") as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open(self.file, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted).decode("utf-8")
        return decrypted


class WakeUpHub:
    """A class used to wake up the hub, create a wake word and
    authenticate it"""
    def __init__(self):
        self.file = "wake_word.txt"

    def auth_wake_word(self, word):
        """Decrypts the wake word set up and stored in a file and compares
        it to the wake word entered by the user"""
        encr = Encryption()
        stored_word = encr.decrypt_wake_word()
        if word == stored_word:
            return True
        return None

    def create_wake_word(self):
        """Asks the user to input wake word, encrypts it and stores it
        in a file"""
        with open(self.file, "w") as f:
            wake_word = input("Please create a custom wake",
                              "word by entering it below\n>>>> ")
            encr = Encryption()
            encr.generate_key()
            f.write(wake_word)
            f.close()
            encr.encrypt_wake_word()

    def wake_up(self):
        """If the wake word file is not 0 (wake word exists), asks the
        userto input the wake word. Otherwise, asks the user to create
        a wake word"""
        if os.stat(self.file).st_size == 0:
            self.create_wake_word()
            return self.wake_up()
        else:
            wake_word = input("Please enter wake word below:\n>>>>> ")
            return self.auth_wake_word(wake_word)


def on_connect(client, userdata, flags, r_c):
    """Advises user whether they are connected to the MQTT broker or not"""
    if r_c == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK_STATUS", qos=2)
    else:
        print("Failed to connect, return code %d\n", r_c)


def on_message(client, userdata, message):
    """Producer activity - reads the data from the MQTT server and puts
    it into the message queue to be processed by the consumer thread"""
    MsgQ.put(message.payload.decode())


def consumer():
    """Define the consumer thread to read messages from the message queue"""
    while True:
        msg = MsgQ.get()
        if msg == "Locked":
            print("The door is locked")
        elif msg == "Unlocked":
            print("The door is unlocked")
        else:
            print("Unknown command recieved")
        MsgQ.task_done()


def user_action(user_input):
    """Publishes the user's request to lock/unlock to the MQTT broker. If the
    input is invalid, it asks the user to enter a valid option or allows them
    to exit"""
    if user_input.lower() == "lock":
        client.publish("LOCK", "Lock", qos=2)   # Publish 'Lock' to MQTT broker topic 'LOCK'
    elif user_input.lower() == "unlock":
        client.publish("LOCK", "Unlock", qos=2)
    elif user_input.lower() == "exit":
        sys.exit()
    else:
        print("Please enter a valid option below\n-Unlock\n-Lock\n-Exit\n>>>")
        action = input()
        user_action(action)


def broker_auth():
    """Opens the password file where the controller hub user name and the
    password are stored for accessing the MQTT broker"""
    with open("hub_passwordfile.txt") as f:
        lines = f.readlines()
        user = lines[0].strip()
        passwd = lines[1].strip()
    return user, passwd


def user_interface(wakeuptest):
    """Asks user for their input, calls the function to verify user input"""
    wake = WakeUpHub()
    if wakeuptest is False:
        print("What would you like to do?",
              "\n-Unlock\n-Lock\n-Exit\nPlease type your request below\n>>>")
        action = input()
        user_action(action)
    elif wake.wake_up() is True:
        print("What would you like to do?",
              "\n-Unlock\n-Lock\n-Exit\nPlease type your request below\n>>>")
        action = input()
        user_action(action)
    else:
        print("You do not have access")
        sys.exit()


# Set up message queue
MsgQ = Queue()

# Start the consumer thread
t = Thread(target=consumer)
t.daemon = True
t.start()

MQTT_BROKER = "mqtt.aliahmed.app"   # Identifies the MQTT broker location

client = mqtt.Client("Hub-984323")  # Sets up the new client
client.username_pw_set(broker_auth()[0], broker_auth()[1])   # Pass client credentials to MQTT broker
client.connect(MQTT_BROKER)  # Tells the client to connect to the broker

client.on_connect = on_connect
client.on_message = on_message

WAKEUP_TEST_COMPLETE = False    # Sets the initial hub state to not awake

"""Defines a loop which allows the user to lock/unlock the door without having
to enter the wake word each time if the wake word has been authenticated"""
while True:
    if WAKEUP_TEST_COMPLETE is False:
        user_interface(True)
        WAKEUP_TEST_COMPLETE = True
        client.loop_start()
    else:
        time.sleep(1)   # Wait for thread to update status on screen
        user_interface(False)
        client.loop_start()

client.loop_forever()
