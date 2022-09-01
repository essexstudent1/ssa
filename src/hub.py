"""The controller hub script which connects to the MQTT broker and publishes the user's input to the 'LOCK' topic. It also subscribes to the 'LOCK_STATUS' topic
on the MQTT broker which is populated by the smart lock"""
import paho.mqtt.client as mqtt
import hashlib

# non hashed password is SECUREarchitecture2022 for testing

# Identifying online broker location - Eclipse mosquito
#mqttBroker ="mqtt.eclipseprojects.io"
mqttBroker ="0.0.0.0"

# Advises the user whether they are connected to the MQTT broker or not.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe("LOCK_STATUS")
    else:
        print("Failed to connect, return code %d\n", rc)

# Advises the user upon receiving the response from the MQTT broker on the current door status: Locked/Unlocked
def on_message(client, userdata, message):
    if message.payload.decode() == "Locked":
        print ("The door is locked")
        #client.disconnect()
    else:
        print ("The door is unlocked")
        #client.disconnect()

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

# asks user for their input, calls the function to verify the user input
def user_interface():
    if wake_word == 'Wake':
        print ("What would you like to do?\n-Unlock\n-Lock\n-Exit\nPlease type your request below\n>>>")
        action = input()
        user_action(action)
    else:
       print ("You do not have access")
       
# Setting up a new client and telling it to connect to the broker
client = mqtt.Client("Hub-984323")
client.on_connect = on_connect
client.on_message=on_message
client.username_pw_set("hub", password="j6i3dd009153ef76")
client.connect(mqttBroker)

#client.on_connect = on_connect
wake_word = input("Enter wake word:")
user_interface()

client.loop_forever()
