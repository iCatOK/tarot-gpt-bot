#!/usr/bin/env sh

set -e

case "$1" in
    bot)
        exec python app/main.py
        ;;
    *)
        exec "$@"
esac