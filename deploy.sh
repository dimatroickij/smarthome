#!/bin/sh

ssh -o StrictHostKeyChecking=no dimatroickij@$IP_ADDRESS << 'ENDSSH'
  cd /home/dimatroickij/app
  export $(cat .env | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker pull $IMAGE:web
  docker pull $IMAGE:nginx
  docker pull library/rabbitmq:3.8-management
  docker pull $IMAGE:celery
  docker pull $IMAGE:celery_beat
  docker-compose -f docker-compose.prod.yml up -d
ENDSSH
