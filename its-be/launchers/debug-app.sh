#!/bin/bash

set -m

flask --debug --app be run &
celery -A make_celery worker --loglevel=INFO &
celery -A make_celery beat -S redbeat.RedBeatScheduler --loglevel=INFO &

fg %1
trap 'kill $(jobs -p)' EXIT
