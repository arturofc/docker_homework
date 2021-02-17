#!/bin/bash

/opt/wait-for-it.sh $DB_HOST:$DB_PORT --timeout=5 --strict -- \
    echo "Peforming database migrations.." && \
    flask db upgrade &&
    exec "$@"