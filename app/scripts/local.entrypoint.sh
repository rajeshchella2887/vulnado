#!/bin/sh

sh ./scripts/base-entrypoint.sh local.env local.entrypoint.sh

python manage.py flush --no-input
python manage.py migrate

exec "$@"
