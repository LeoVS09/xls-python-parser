from peewee import *
from database.GroupDB import GroupDB
from database.DayDB import DayDB
from database.LessonDB import LessonDB
from database.data import db

class Database:
    def __init__(self):
        db.connect()


    def save(self,groups):
        groups_db = []
        for group in groups:
            group_db = GroupDB.create(name=group.name)
            for name,day in group.days.items():
                day_db = DayDB.create(name=day.name,group=group_db)
                for time,lessons in day.lessons.items():
                    for lesson in lessons:
                        lesson_db = LessonDB.create(name=lesson.name,
                                                teacher=lesson.teacher,
                                                times=lesson.times,
                                                room=lesson.room,
                                                type=lesson.type,
                                                time=lesson.time,
                                                day=day_db)
