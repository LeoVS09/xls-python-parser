from database.DayDB import DayDB
from database.data import db
from peewee import *





class LessonDB(Model):

    name = CharField()
    teacher = CharField()
    times = BigIntegerField()
    room = CharField()
    type = CharField()
    time = CharField()
    day = ForeignKeyField(DayDB,related_name="lessons")



    def __str__(self):
        return "{\n\"name\": " + self.name + \
               ",\n\"teacher\": " + self.teacher + \
                ",\n\"week\": " + str(self.get_times()) + \
                ",\n\"room\": " + self.room + \
                ",\n\"type\": " + self.type + "\n}"

    class Meta:
        database = db

    def save(self, force_insert=False, only=None):
        if not self.table_exists():
            self.create_table()
        super(LessonDB,self).save(force_insert,only)