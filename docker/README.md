Prerequisites
------------
- Jetson Orin Nano with updated Ubuntu - version (e.g. 20.04.6 LTS) 
- Updated docker-compose version - (v2.24.5)



Building Image
--------------
- Open a terminal window.
- Make sure you are in the `./docker` directory of the cloned source tree. 
- Run this command : `sudo docker-compose build`


Running Redis Server
--------------------
- Run this command : `sudo docker-compose up -d redis`
    - OPTIONAL. To login interactively into redis server container and query the database using the redis-cli
        - Run this command : `sudo docker exec -it redis sh`
        - Once inside the container, run this command : `redis-cli -h localhost`
        - To exit the instance, type : `quit` then `type exit`

Running MQTT Server
-------------------
- Run this command : `sudo docker-compose up -d mqtt5`
    - OPTIONAL. To login interactively into the MQTT server container and connect to the `PUB` topic 
        - Run this command : `sudo docker exec -it mqtt5 sh`
        - Once inside the container, run this command : `mosquitto_sub -h localhost -t pub -u admin -P admin`
        - To exit the instance, type : `Ctrl+C` and `exit`

Running a mqtt_client Example 
-------------------------------
- Open a new terminal window.
- Run this command : `sudo docker-compose run --rm mqtt_client`
- Once inside the container, type : `python ./mqtt_client_decode_i10/client.py`
- To exit the instance, type : `Ctrl+C` and `exit`
    - OPTIONAL. For i10 beacon. Run a parameterized shell script to start the container. 
        - `cd ../src/bash/`
        - `sh mqtt_i10_client.sh`
    - Optional. For industrial temperature beacon. Run a parameterized shell script to start the container.
        - `cd ../scr/bash`
        - `sh mqtt_temp_client.sh` 
