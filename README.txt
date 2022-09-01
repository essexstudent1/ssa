How to use this demo in Codio:
1) Create a new codio project
2) Install mosquitto server: sudo apt-get install mosquitto
3) Install mosquitto clients: sudo apt install mosquitto-clients
4) Create a new mosquitto server config file: sudo nano /etc/mosquitto/conf.d/my.conf
  a) Paste in the following:
    allow_anonymous false
    password_file /etc/mosquitto/passwd
  b) Save and close the file
5) Edit the password file: sudo nano /etc/mosquitto/passwd
  a) Paste in the following:
    hub:j6i3dd009153ef76
    lock:k3dd651mniofd90q
   b) Save and close the file
6) Encrypt the passwords: sudo mosquitto_passwd -U /etc/mosquitto/passwd
7) Restart mosquitto: sudo systemctl restart mosquitto
