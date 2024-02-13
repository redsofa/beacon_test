#!/bin/sh

# Command to start the docker container 
sudo docker-compose \
	--project-directory ../../docker \
	run \
	--rm mqtt_client \
	python /src/python/mqtt_client_decode_i10/client.py \
		--beacon_mac C300000A5F41 \
		--loglevel DEBUG \
		--mqtt_server_address mqtt5
