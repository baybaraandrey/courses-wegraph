#!/bin/bash

exec docker-compose -f dev.yml run --rm web courses makemigrations $@
