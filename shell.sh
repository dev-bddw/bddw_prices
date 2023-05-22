#!/bin/sh

sudo docker-compose -f local.yml run --rm django python manage.py shell_plus
