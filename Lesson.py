import re
from srl import SRL
import data as consts

def srl_capture(name, string):
    return (name, SRL("capture (" + string + ") as \"" + name + "\""))


class Lesson:
    # TODO: add кр. в парсинг и расчет недель
    # TODO: add зачет в расчет типов\
    # TODO: add понимание кабинета если он меняется на разных неделях
    filter = dict([
        srl_capture("week", """letter from а to я exactly 3 times,
                                    literally "/нед" once"""),

        srl_capture("room", """any of((literally "а" optional,
                            literally "." optional,
                            digit once or more,
                            literally "/" once,
                            digit once or more,
                            (literally "/" once) optional,
                            (digit once or more) optional),
                            literally "спортзал") """),

        srl_capture("type", """any of(literally "лекция",
                                    literally "пр",
                                    literally "лаб",
                                    literally "лб")"""),

        srl_capture("week_n", """any of (((any of (digit, literally ",", literally "-")) once or more,
                                        literally "н" once),
                                        (digit once or more,
                                        literally "-",
                                        digit once or more))""")
    ])

    plus2end = str(SRL('literally "+" once, anything once or more, must end'))

    def __init__(self, name=None, teacher=None, times=None, room=None, type=None, string=None):
        if string is not None:
            name, teacher, times, room, type = self._parse(self, string)
        self.name = name
        self.teacher = teacher
        self.times = times
        self.room = room
        self.type = type

    @staticmethod
    def _parse(self, string):

        string = re.sub(self.plus2end, '', string).strip()

        for name in consts.NOT_PARSING_NAMES_OF_LESSONS:
            if string.find(name) != -1:
                return (name, "lol", "lol", "lol", "lol")

        alpha = self._alpha_search(self, string)

        data = self.clear_line(self, string, alpha).split(",")
        for i in range(len(data)):
            data[i] = data[i].strip()

        for key, item in alpha.items():
            if item in data: data.remove(item)

        return (data[0], data[1] if len(data) >= 2 else "lol",
                alpha["week"] + " " + alpha["week_n"], alpha["room"], alpha["type"])

    @staticmethod
    def clear_line(self,string,data):

        for item in data:
            if item == "lol": continue
            n = string.find(item)

            if n != -1:
                beg = ""
                if n == 0 or n == 1:
                    beg = string[:n]
                else:
                    i = 0
                    if string[n-1] == " " or string[n-1] == ",": i -= 1
                    if string[n-2] == ",": i -= 1
                    beg = string[:n+i]
                end = string[n+len(item):]
                string = beg + end

        return string

    @staticmethod
    def _alpha_search(self, string):

        result = {}
        for key, srl in self.filter.items():
            if key == "week":
                continue
            r = srl.search(string)
            if r:
                r = r.group(0)
            else:
                r = "lol"
                print("Error when alpha parse: ", string, "in key: " + key)
            result[key] = r

        r = self.filter["week"].search(string)
        if not r:
            r = "lol"
            if result["week_n"] == "lol":
                print("Error when alpha parse: ", string, "in key: week")
        else:
            r = r.group(0)
        result["week"] = r

        return result

    def __str__(self):
        return "{\n\"name\": " + self.name + \
               ",\n\"teacher\": " + self.teacher + \
                ",\n\"week\": " + self.times + \
                ",\n\"room\": " + self.room + \
                ",\n\"type\": " + self.type + "\n}"
