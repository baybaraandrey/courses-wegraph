#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


POSTGRES_USER=${POSTGRES_USER:-courses}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-courses}
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-courses}
POSTGRES_TEST_DB=${POSTGRES_TEST_DB:-courses_test}


postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}

RETRIES="${RETRIES:-10}"

function wait_for_postgres {
  until postgres_ready || [ $RETRIES -eq 0 ] ; do
    >&2 echo "Waiting for PostgreSQL to become available $((RETRIES--))"
    sleep 1
  done

  if [ $RETRIES -le 0 ]; then
    echo "TIME_OUT"
    exit 1
  else
      >&2 echo 'PostgreSQL is available'
  fi
}

BIN="$(dirname "$(realpath "$0")")"
ROOT="$(dirname "$BIN")"

case "$1" in
    linter)
        shift
        exec "$BIN/linter.bash" "$@"
    ;;
    tests)
        shift
        exec "$BIN/tests.bash" "$@"
    ;;
    dev_server)
        wait_for_postgres
        shift
        exec "$BIN/dev_server.bash" "$@"
    ;;
    prod_server)
        wait_for_postgres
        shift
        exec "$BIN/prod_server.bash" "$@"
    ;;
    courses)
        wait_for_postgres
        shift
        exec courses "$@"
    ;;
    *)
        exec "$@"
    ;;
esac
