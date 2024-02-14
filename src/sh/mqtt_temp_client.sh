#!/bin/sh

# Command to start the docker container 
sudo docker-compose \
	--project-directory ../../docker \
	run \
	--rm mqtt_client \
	python /src/python/mqtt_client_decode_temp/client.py \
		--beacon_mac AC233FAE2EF7 \
		--loglevel DEBUG \
		--mqtt_server_address mqtt5 \
		--mqtt_server_user admin \
		--mqtt_server_password admin \
		--mqtt_topic pub \
		--mqtt_port 1883 \
		--mqtt_keep_alive 60
