from peewee import *
from database.GroupDB import GroupDB
from database.data import db


class DayDB(Model):

    name = CharField()
    group = ForeignKeyField(GroupDB, related_name="days")

    class Meta:
        database = db

    def save(self, force_insert=False, only=None):
        if not self.table_exists():
            self.create_table()
        super(DayDB,self).save(force_insert,only)