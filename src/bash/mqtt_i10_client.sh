#!/bin/bash

# Command to start the docker container 
sudo docker-compose \
	--project-directory ../../docker \
	run \
	--rm mqtt_client \
	python /src/python/mqtt_client_decode_i10/client.py \
		--beacon_mac C300000A5F41 \
		--loglevel DEBUG \
		--mqtt_server_address mqtt5 \
		--mqtt_server_user admin \
		--mqtt_server_password admin \
		--mqtt_input_topic pub \
		--mqtt_output_topic i10 \
		--mqtt_port 1883 \
		--mqtt_keep_alive 60
