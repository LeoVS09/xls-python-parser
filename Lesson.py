class Lesson:
    def __init__(self, name=None, teacher=None, times=None, room=None, type=None, string=None):
        if string is not None:
            name, teacher, times, room, type = self._parse(string)
        self.name = name
        self.teacher = teacher
        self.times = times
        self.room = room
        self.type = type

    def _parse(self, string):
        return ("lol", "lol", "lol", "lol", "lol")

