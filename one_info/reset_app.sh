#!/bin/sh

python manage.py reset membership
python manage.py syncdb
python manage.py loaddata data_setup.json
python manage.py runserver

