from entities.Day import Day


class Group:

    def __init__(self,name):
        super()
        self.name = name
        self.days = {}


    def add_lesson(self,day,time,lesson):
        if lesson == "" or lesson is None: return
        if day in self.days:
            self.days[day].add_lesson(time,lesson)
        else:
            self.days[day] = Day(day)

