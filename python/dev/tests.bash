#!/bin/bash

exec docker-compose -f dev.yml run --rm -e DJANGO_SETTINGS_MODULE=config.settings.testing web tests $@
