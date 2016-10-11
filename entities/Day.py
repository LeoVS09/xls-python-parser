import re

from entities.Lesson import Lesson
from srl import SRL


class Day:
    whitespace = str(SRL("whitespace"))
    dot = str(SRL("literally \".\""))
    def __init__(self, name):
        super()
        self.name = self._parse_name(self,name)
        self.lessons = {}

    @staticmethod
    def _parse_name(self, string):
        result = re.sub(self.whitespace,'',string)
        return result

    def add_lesson(self, time, lesson):
        time = self._parse_time(self, time)
        if time not in self.lessons:
            self.lessons[time] = [Lesson(string=lesson,time=time)]
        else:
            self.lessons[time].append(Lesson(string=lesson,time=time))

    @staticmethod
    def _parse_time(self, time):
        time = re.sub(self.dot,":",time).strip()
        return time

