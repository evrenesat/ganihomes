__author__ = 'Evren Esat Ozkan'
from django.db import models

class EtkinManager(models.Manager):
#    def __init__(self, tip):
#        self.tip = tip
#        super(EtkinManager, self).__init__()
    def get_query_set(self):
        return super(EtkinManager, self).get_query_set().filter(etkin=True)
