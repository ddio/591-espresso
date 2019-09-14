import json
from os import path
from functools import partial
from datetime import datetime
from peewee import Model, AutoField, CharField, DateTimeField, \
    ForeignKeyField
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase(path.join(path.dirname(__file__), '../data/db.sqlite'))

friendly_json_dumps = partial(json.dumps, ensure_ascii=False)

class Job(Model):
    id = AutoField()
    url = CharField()
    cities = JSONField(null=True, json_dumps=friendly_json_dumps)
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
    list_meta = JSONField(null=True, json_dumps=friendly_json_dumps)
    detail_meta = JSONField(null=True, json_dumps=friendly_json_dumps)
    rough_gps = JSONField(null=True, json_dumps=friendly_json_dumps)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(House, self).save(*args, **kwargs)

    class Meta:
        database = db
        indexes = (
            (('job_id', 'house_id'), True),
        )

db.create_tables([Job, House])
