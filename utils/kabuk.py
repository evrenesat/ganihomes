'''

./manage.py shell komutu ile kabugu actiktan sonra asagidaki komutu verirseniz hayatiniz daha guzel olacak. gercekten...

from utils.kabuk import *

'''
try:
    from django.conf import settings
    settings.DEBUG=True
    from django.db import connection, models

    # Load each installed app and put models into the global namespace.
    for app in models.get_apps():
        exec("from %s import *" % app.__name__)

    def sonarzu():
        "yapilan son sql sorgusunu dondurur."
        return connection.queries[-1]

    #===================================================
    # Add commonly used modules, classes, functions here
    #===================================================
    from django import forms
    import os
    from datetime import datetime
except:
    pass