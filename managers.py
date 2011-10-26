__author__ = 'Evren Esat Ozkan'
from django.db import models

class ActiveManager(models.Manager):
#    def __init__(self, tip):
#        self.tip = tip
#        super(EtkinManager, self).__init__()
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(active=True)
