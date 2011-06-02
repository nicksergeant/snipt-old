#!/usr/bin/env bash

gunicorn -c gunicorn.conf.py debug_wsgi:application
