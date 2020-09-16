#!/usr/bin/env bash
supervisorctl -c /moss/supervisord.conf restart celery-worker-asyncFunction
supervisorctl -c /moss/supervisord.conf restart celery-worker-cronJob
