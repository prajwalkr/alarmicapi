from django.db.models import *

class user(Model):
	phNum = IntegerField(primary_key = True)
	gcmId = CharField(max_length = 100)
	nick = CharField(max_length = 50)

