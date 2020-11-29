#!/bin/bash

set -e

BIN="$(dirname "$(realpath "$0")")"
ROOT="$(dirname "$BIN")"

case "$1" in
    upgrade)
        UPGRADE="--upgrade"
    ;;
    *)
        UPGRADE=""
    ;;
esac

for f in $ROOT/requirements/*.in; do
    pip-compile --no-annotate \
                --generate-hashes \
                --no-header \
                $UPGRADE \
                -o "${f%.in}.txt" \
                -q \
                "$f"
done
