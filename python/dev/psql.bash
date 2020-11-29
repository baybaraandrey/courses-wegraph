#!/bin/bash

exec docker-compose -f dev.yml run --rm postgres-dev psql postgres://courses:courses@postgres-dev:5432/courses $@
