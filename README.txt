How to use this demo in Codio:
1) Create a new codio project
2) Install mosquitto server: sudo apt-get install mosquitto
3) Install mosquitto clients: sudo apt install mosquitto-clients
4) Create a new mosquitto server config file: sudo nano /etc/mosquitto/conf.d/my.conf
  a) Paste in the following:
    allow_anonymous false
    password_file /etc/mosquitto/passwd
  b) Save and close the file

