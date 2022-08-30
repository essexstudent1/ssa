"""MQTT publisher which publishes smart lock status to the lock topic"""
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

# Identifying online broker location - Eclipse mosquito
mqttBroker ="mqtt.eclipseprojects.io"

# Setting up a new client and telling it to connect to the broker
client = mqtt.Client("Lock")
client.connect(mqttBroker)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("LOCK_STATUS")

def on_message(client, userdata, message):
    if message.payload.decode() == "Locked":
        print ("The door is locked")
        client.disconnect()
    else:
        print ("The door is unlocked")
        client.disconnect()

# takes user input and publishes it to the broker
def user_action(user_input):
    if user_input.lower() == "lock":
        client.publish("LOCK", "Lock")
        client.on_message=on_message
    elif user_input.lower() == "unlock":
        client.publish("LOCK", "Unlock")
        client.on_message = on_message
    elif user_input.lower() == "exit":
        exit()
    else:
        print ("Please enter a valid option below\n>>>")
        action = input()
        user_action(action)

# asks user for their input, calls the function to verify the user input
def user_interface():
    if wake_word == 'Wake':
        print ("What would you like to do?\n-Unlock\n-Lock\n-Exit\nPlease type your request below\n>>>")
        action = input()
        user_action(action)
    else:
       print ("You do not have access")

client.on_connect = on_connect
wake_word = input("Enter wake word:")
user_interface()

client.loop_forever()
