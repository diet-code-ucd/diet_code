#!/bin/bash

set -m

flask run -p 8080 --debug  &
celery -A make_celery worker --loglevel=INFO &
celery -A make_celery beat -S redbeat.RedBeatScheduler --loglevel=INFO &

fg %1
trap 'kill $(jobs -p)' EXIT
