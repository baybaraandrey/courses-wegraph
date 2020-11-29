#!/bin/bash

exec docker-compose -f dev.yml up --remove-orphans
