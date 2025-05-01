from loguru import logger
from peewee import (
    MySQLDatabase,
    CompositeKey,
    Model,
    CharField,
    TextField,
    DateTimeField,
    IntegerField,
    BooleanField,
)
from playhouse.shortcuts import ReconnectMixin

from src.config import settings


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


db = ReconnectMySQLDatabase(
    database=settings.database,
    host=settings.database_host,
    port=settings.database_port,
    user=settings.database_user,
    password=settings.database_passwd,
    charset="utf8mb4",
)

if not db.connect():
    logger.error("Database connection failed")
    raise ValueError("Database connection failed")


class Anno(Model):
    language = CharField()
    summary = TextField()
    details = TextField()
    start = DateTimeField()
    end = DateTimeField()

    class Meta:
        database = db
        table_name = "anno"


class Plan(Model):
    plan_index = IntegerField()
    type_id = CharField()
    plan_id = CharField()
    title = TextField()
    price = CharField()
    original_price = CharField()
    popular = IntegerField()
    available = BooleanField()
    afdian_id = CharField()
    yimapay_id = CharField()

    class Meta:
        database = db
        table_name = "plan"

class Project(Model):
    type_id = CharField()
    proj_index = IntegerField()
    rid = CharField()
    name = CharField()
    desc = TextField()
    image = TextField()
    url = TextField()
    platform = TextField()
    download = BooleanField()
    available = BooleanField()

    class Meta:
        database = db
        table_name = "project"

class ICP(Model):
    domain = CharField()
    beian = CharField()
    entity = CharField()
    url = CharField()

    class Meta:
        database = db
        table_name = "icp"

Anno.create_table()
Plan.create_table()
Project.create_table()
ICP.create_table()