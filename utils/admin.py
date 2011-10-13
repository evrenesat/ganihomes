from django.contrib.admin.sites import AlreadyRegistered

__author__ = 'Evren Esat Ozkan'


def admin_register(admin, namespace):
    '''convenience function to easily register admin classes

    :param admin: result of 'from django.contrib import admin'
    :param namespace: must take a locally called globals

    usage::

        # should be at the end of the admin.py file
        # globals must be called locally as below
        admin_register(admin, namespace=globals())

    '''
    for name, model_admin in namespace.copy().iteritems():
        if name.endswith("Admin"):
            model = namespace[name[:-5]]
            try: admin.site.register(model, model_admin)
            except AlreadyRegistered:
                pass
            except: raise
