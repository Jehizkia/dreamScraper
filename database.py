from peewee import *

db = MySQLDatabase('dreams', user='root', password='', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class Dream(BaseModel):
    title = CharField()
    description = TextField()
    category = CharField()
    played_time = IntegerField()
    played_times_by = IntegerField()
    thumbs_up = IntegerField()
    author = CharField()


db.connect()
db.create_tables([Dream])
