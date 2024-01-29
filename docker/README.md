Building Image
--------------
- Open a terminal window.
- Make sure you are in the `./docker` directory of the cloned source tree. 
- Run this command : `docker-compose build`



Running MQTT Server
-------------------
- Run this command : `docker-compose up mqtt5`



Running PoC
-----------
- Open a new terminal window.
- Run this command : `docker-compose run --name poc_server --rm poc_server`
- Run this command (inside container) : `cd src/python/mqtt_client_decode_temp`
- Run this command (inside contaienr) : `python client.py`
