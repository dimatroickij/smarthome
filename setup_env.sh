#!/bin/sh

echo CELERY_BROKER_URL=$CELERY_BROKER_URL >> .env
echo CELERY_RESULT_BACKEND=$CELERY_RESULT_BACKEND >> .env
echo CELERY_TIMEZONE=$CELERY_TIMEZONE >> .env
echo DEBUG=$DEBUG >> .env
echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS >> .env
echo EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD >> .env
echo EMAIL_HOST_USER=$EMAIL_HOST_USER >> .env
echo RABBITMQ_DEFAULT_USER=$RABBITMQ_DEFAULT_USER >> .env
echo RABBITMQ_DEFAULT_PASS=$RABBITMQ_DEFAULT_PASS >> .env
echo SECRET_KEY=$SECRET_KEY >> .env
echo SITE_PROTOCOL=$SITE_PROTOCOL >> .env
echo SITE_URL=$SITE_URL >> .env
echo SQL_DATABASE=$SQL_DATABASE >> .env
echo SQL_ENGINE=$SQL_ENGINE >> .env
echo SQL_HOST=$SQL_HOST >> .env
echo SQL_PASSWORD=$SQL_PASSWORD >> .env
echo SQL_PORT=$SQL_PORT >> .env
echo SQL_USER=$SQL_USER >> .env
echo CI_REGISTRY_USER=$CI_REGISTRY_USER   >> .env
echo CI_JOB_TOKEN=$CI_JOB_TOKEN  >> .env
echo CI_REGISTRY=$CI_REGISTRY  >> .env
echo IMAGE=$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME >> .env

