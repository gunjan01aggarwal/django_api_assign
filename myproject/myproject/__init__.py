from  __future__ import absolute_import,unicode_literals
from celery.app.base import Celery

#This will make sure the app is always imported when 
#django starts so that shared_task will use this app.
__all__ = ('Celery',)