#!/bin/sh

sh ./scripts/base-entrypoint.sh prod.env prod.entrypoint.sh

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
