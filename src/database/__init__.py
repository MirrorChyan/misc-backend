from loguru import logger
from peewee import (
    MySQLDatabase,
    CompositeKey,
    Model,
    CharField,
    TextField,
    DateTimeField,
    IntegerField,
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
    platform = CharField()
    plan_id = CharField()
    type_id = CharField()
    popular = IntegerField()

    class Meta:
        database = db
        table_name = "plan"

Anno.create_table()
Plan.create_table()
