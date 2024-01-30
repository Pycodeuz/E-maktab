from django.db.models import Model, CharField, IntegerField, TextField


class School(Model):
    name = CharField(max_length=50)
    number = IntegerField()
    address = CharField(max_length=255)
    description = TextField()
