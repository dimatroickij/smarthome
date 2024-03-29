#!/bin/sh

ssh -o StrictHostKeyChecking=no dimatroickij@$IP_ADDRESS << 'ENDSSH'
  cd /home/dimatroickij/applications/smarthome
  export $(cat .env | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker pull $IMAGE:smarthome
#  docker pull $IMAGE:smarthome-nginx
  docker pull library/rabbitmq:3.8-management
  docker-compose -f docker-compose.prod.yml up -d
ENDSSH
