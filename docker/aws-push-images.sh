#!/bin/bash
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 305402192421.dkr.ecr.sa-east-1.amazonaws.com

docker push 305402192421.dkr.ecr.sa-east-1.amazonaws.com/sibila-fastapi:latest
docker push 305402192421.dkr.ecr.sa-east-1.amazonaws.com/sibila-orientdb:latest
