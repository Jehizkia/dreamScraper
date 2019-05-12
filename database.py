from peewee import *

db = MySQLDatabase('dreams', user='root', password='', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class Dream(BaseModel):
    name = CharField(unique=True)


db.connect()
db.create_tables([Dream])
