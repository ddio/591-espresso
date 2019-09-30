import json
from os import path
from functools import partial
from datetime import datetime
from peewee import Model, AutoField, CharField, DateTimeField, \
    ForeignKeyField, IntegerField, BooleanField
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase(path.join(path.dirname(__file__), '../data/db.sqlite'))

friendly_json_dumps = partial(json.dumps, ensure_ascii=False)

class TimestampModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

class Job(TimestampModel):
    id = AutoField()
    url = CharField()
    cities = JSONField(null=True, json_dumps=friendly_json_dumps)
    opts = JSONField(null=True, json_dumps=friendly_json_dumps)

    class Meta:
        database = db

class House(TimestampModel):
    job_id = ForeignKeyField(Job, backref='houses')
    house_id = CharField()
    list_meta = JSONField(null=True, json_dumps=friendly_json_dumps)
    detail_meta = JSONField(null=True, json_dumps=friendly_json_dumps)
    rough_gps = JSONField(null=True, json_dumps=friendly_json_dumps)

    class Meta:
        database = db
        indexes = (
            (('job_id', 'house_id'), True),
        )

class HouseStats(TimestampModel):
    job_id = ForeignKeyField(Job, backref='houses')
    house_id = CharField()
    list_count = IntegerField(default=0)
    detail_count = IntegerField(default=0)
    gps_count = IntegerField(default=0)
    is_vip = BooleanField(default=False)

    class Meta:
        database = db
        indexes = (
            (('job_id', 'house_id'), True),
        )

db.create_tables([Job, House, HouseStats])
