"""
WSGI config for conconexp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

import sys
import site
#sys.stderr.write(str(sys.version_info))
sys.stderr.write(str(sys.executable))


from django.core.wsgi import get_wsgi_application

# add the conconexp project path into the sys.path
sys.path.append('/home/site/concon-front-end-master/conconexp')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/site/concon-front-end-master/conconexp/conconenv/lib/python2.7/site-packages')

# poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")

# site.addsitedir('/usr/lib/python2.7/dist-packages')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conconexp.settings")


application = get_wsgi_application()
