# Example Overview
This project is an example project that enables the collection of data from 
sensor beacons via an ethernet Bluetooth gateway and MQTT server. The sensors 
are connected to an ethernet gateway. The gateway receives sensor readings 
and sends them to an MQTT sever's <b>PUB</b> topic. The MQTT server is 
configured to run in a Docker container. There are Python <b>(e.g. client.py)</b> 
scripts, also encapsulated in Docker containers, that are setup to 
subscribe to this <b>PUB</b> topic and print decoded 
messages to the screen. Note that all containers run on Jetson Nano Orin host.

![alt Intro](https://github.com/redsofa/beacon_test/blob/aarch64/beacon_test.png)


# Running Python Examples

![alt Example](https://github.com/redsofa/beacon_test/blob/main/beacon_test.gif)


# Web Client

![alt Web Client](https://github.com/redsofa/beacon_test/blob/aarch64/updating.gif)


# To Run the Examples

* See the [./docker/README.md](./docker/README.md) file.

