from peewee import *
from database.data import db

class GroupDB(Model):

    name = CharField(index=True,unique=True)

    class Meta:
        database = db

    def save(self, force_insert=False, only=None):
        if not self.table_exists():
            self.create_table()
        super(GroupDB,self).save(force_insert,only)