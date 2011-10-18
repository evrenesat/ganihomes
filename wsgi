import os, sys
os.environ['PYTHON_EGG_CACHE'] = '/tmp/tafteggs'
sys.stdout = sys.stderr
base=os.path.dirname(__file__)
sys.path.insert(0,base)
sys.path.append(os.path.dirname(base))
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % os.path.basename(base)
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
