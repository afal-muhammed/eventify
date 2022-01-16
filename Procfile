web: gunicorn eventwiz.wsgi --log-file -
web: python manage.py collectstatic --no-input; gunicorn eventwiz.wsgi --log-file - --log-level debug