#!/bin/bash

docker-compose -f dev.yml run --rm web courses createsuperuser
