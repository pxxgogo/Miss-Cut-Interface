#!/usr/bin/env bash
celery -A web worker -Q MC_util --concurrency=10 -l info -E -n MC_util@%h