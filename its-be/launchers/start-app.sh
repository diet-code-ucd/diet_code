#!/bin/bash

set -m

waitress-serve --port=5000 --call 'be:create_app' &
celery -A make_celery worker --loglevel=INFO &
celery -A make_celery beat -S redbeat.RedBeatScheduler --loglevel=INFO &

fg %1
trap 'kill $(jobs -p)' EXIT
