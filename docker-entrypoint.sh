#!/bin/sh


python manage.py migrate

echo "from django.contrib.auth.models import User; \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'mucahitmustafay@gmail.com', 'Admin123')" \
| python manage.py shell

python manage.py runserver 0.0.0.0:8000
