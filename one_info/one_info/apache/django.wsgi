import os
import sys
import django.core.handlers.wsgi

path = '/var/www'
site_path='/var/www/one_flow'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(site_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'one_flow.settings'

application = django.core.handlers.wsgi.WSGIHandler()
