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


Running PoC 
-----------
- Open a new terminal window.
- Run this command `sudo docker-compose run --rm poc_server`


