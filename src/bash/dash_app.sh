#!/bin/bash

# Command to start the docker container 
sudo docker-compose \
	--project-directory ../../docker \
	run \
	-p 8080:8080 \
	--name dash_app \
	--rm dash_app \
	hupper -m dash_app2.app

