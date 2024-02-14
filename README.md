# Example Overview
This project is an example project that enables the collection of data from a temperature and humidity sensor via an ethernet bloothooth gateway and MQTT server.
The sensor is connected to an ethernet gateway. The gateway receives sensor readings and then sends them to an MQTT sever's <b>PUB</b> topic. The MQTT server is configured to run in a Docker container.
There is a Python <b>client.py</b> script, that is also running in a container, that is setup to subscribe to this <b>PUB</b> topic and print decoded messages to the screen. Containers run on Jetson Nano Orin host.

![alt Intro](https://github.com/redsofa/beacon_test/blob/main/beacon_test.png)



# A Running Example

![alt Intro](https://github.com/redsofa/beacon_test/blob/main/intro.png)



# To Run the Example

* See the [./docker/README.md](./docker/README.md) file.

