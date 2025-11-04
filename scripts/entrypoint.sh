#!/usr/bin/env bash
set -e
export PORT="${PORT:-8080}"
exec gunicorn -w 2 -b 0.0.0.0:${PORT} main:app