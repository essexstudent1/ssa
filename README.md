# ssa
Assignment for  SSA_PCOM7E August 2022- 
- MQTT is a compact client-server publish/subscribe messaging protocol that is designed for erratic or latency-prone networks. Applications like as telemetry, sensor networks, smart metering, home automation, messaging, and notification services are all appropriate fits for this protocol.
The Gateway offers straightforward integration APIs and includes typical Thingsboard-related functions including device setup, local data persistence and delivery, message converters, and others.
In order to handle data from devices, you can also create a custom converter that will take the data from the device and convert it to a uniform format before delivering it to the ThingsBoard cluster.

PORT: Default 1883 MQTT broker port , encrypted port is 8883

hello username for authorized connections.
hello password for authorized connections.

A minimal MQTT control message can be as little as two bytes of data. Almost 256 megabytes of data can fit in a control message if necessary. There are fourteen defined message types used to connect and disconnect a client from a broker, to publish data, to acknowledge receipt of data, and to supervise the connection between client and server.
MQTT depends on the TCP protocol for data delivery. MQTT-SN, a variation, is used with Bluetooth or UDP as an alternative transport.
MQTT sends connection credentials in plain text format and does not include any measures for security or authentication. This may be supplied by utilizing TLS to encrypt and safeguard the sent information against interception, alteration or forgery.

The MQTT broker is a piece of software that runs on a computer, either locally or in the cloud. It may be created by the user themselves or hosted by a third party. It is available in both open source and proprietary implementations.

The broker functions as a post office. MQTT clients don't use a direct connection address of the intended recipient, but use the subject line called "Topic". All communications for that subject are made available to subscribers in their entirety. Multiple clients can subscribe to a topic from a single broker (one to many capability), and a single client can register subscriptions to topics with multiple brokers (many to one) (many to one).
