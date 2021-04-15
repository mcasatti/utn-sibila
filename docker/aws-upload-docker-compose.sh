#!/bin/bash
scp -i ./base-aws-key-pair.pem ./docker-compose-aws.yml ec2-user@18.229.177.23:/home/ec2-user/docker-compose.yml

