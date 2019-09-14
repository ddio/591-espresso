from os import path
from datetime import datetime
from peewee import Model, AutoField, CharField, DateTimeField, \
    ForeignKeyField
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase(path.join(path.dirname(__file__), '../data/db.sqlite'))

class Job(Model):
    id = AutoField()
    url = CharField()
    cities = JSONField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Job, self).save(*args, **kwargs)

    class Meta:
        database = db

class House(Model):
    job_id = ForeignKeyField(Job, backref='houses')
    house_id = CharField()
    list_meta = JSONField(default=None)
    detail_meta = JSONField(default=None)
    rough_gps = JSONField(default=None)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

db.create_tables([Job, House])
