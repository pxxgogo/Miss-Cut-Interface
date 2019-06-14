#!/usr/bin/env bash
celery -A kernel_utils worker -Q MC_util --concurrency=5 -l info -E -n MC_util@%h