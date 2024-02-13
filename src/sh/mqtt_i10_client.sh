#!/bin/sh

# Command to start the docker container 
sudo docker-compose \
	--project-directory ../../docker \
	run \
	--rm mqtt_client \
	python /src/python/mqtt_client_decode_i10/client.py \
		--beacon_mac 10.1.1.1.2 \
		--loglevel DEBUG \
		--mqtt_server_address mqtt5
