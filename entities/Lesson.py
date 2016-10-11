import re

import data as consts
from srl import SRL


def srl_capture(name, string):
    return (name, SRL("capture (" + string + ") as \"" + name + "\""))


class Lesson:
    # TODO: add кр. в парсинг и расчет недель
    # TODO: add зачет в расчет типов\
    # TODO: add понимание кабинета если он меняется на разных неделях


    filter = dict([
        srl_capture("week", """any of((letter from а to я exactly 3 times,
                                    literally "/нед" once),
                                    literally "еж")"""),

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
    slash_ned = str(SRL('literally "/нед"'))
    def __init__(self, name=None, teacher=None, times=None, room=None, type=None, string=None,time=None):
        super()
        if string is not None:
            name, teacher, times, room, type = self._parse(self, string)
        self.name = name
        self.teacher = teacher
        self.times = times
        self.room = room
        self.type = type
        self.time = time

    @staticmethod
    def _parse(self, string):

        string = re.sub(self.plus2end, '', string).strip()

        for name in consts.NOT_PARSING_NAMES_OF_LESSONS:
            if string.find(name) != -1:
                return (name, "lol", self._parse_times(self,"еж","lol"), "lol", "lol")

        alpha = self._alpha_search(self, string)

        data = self._clear_line(self, string, alpha).split(",")
        for i in range(len(data)):
            data[i] = data[i].strip()

        for key, item in alpha.items():
            if item in data: data.remove(item)
        alpha.update({"name": data[0],
                      "teacher": data[1] if len(data) >= 2 else "lol"})
        result = self._clear_data(self, alpha)

        result["week"] = self._parse_times(self,result["week"],result["week_n"])
        return (result["name"], result["teacher"], result["week"], result["room"], result["type"])

    @staticmethod
    def _clear_line(self,string,data):

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
    def _clear_data(self,data):
        result = {}
        for key, item in data.items():
            result[key] = item
        result["room"] = self._clear_room(self,result["room"])
        return result

    @staticmethod
    def _clear_room(self, string):
        return string

    @staticmethod
    def _parse_times(self,week,numbers):
        result = int("11111111111111111111111111111111",2)
        week.strip()
        week = re.sub(self.slash_ned,"",week)
        if week == "еж":
            result = int("11111111111111111111111111111111",2)
            # print("parse time:",week,numbers,result)
        elif week == "чет":
            result = int("10101010101010101010101010101010",2)
        elif week == "неч":
            result = int("1010101010101010101010101010101",2)
            # print("Error when parse week",week,numbers,self.slash_ned)
        if numbers == "lol":
            return result
        numbers = numbers.split(",")
        res_num = 0
        for i in range(len(numbers)):
            numbers[i] = numbers[i].strip()
            dash = numbers[i].find("-")
            if dash != -1:
                beg = int(numbers[i][:dash])
                if numbers[i][-1] == "н":
                    end = int(numbers[i][dash+1:-1])
                else:
                    end = int(numbers[i][dash + 1:])
                for n in range(beg,end):
                    res_num = res_num | n
            else:
                if numbers[i] is not None and numbers[i] != "":
                    res_num = res_num | int(numbers[i]  if numbers[i][-1] != "н" else numbers[i][:-1])

        return result & res_num

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

    def get_times(self):

        num = self.times
        result = []
        k = 1
        while num != 0:
            res = num % 2
            if res != 0:
                result.append(k)
            k += 1
            num //= 2

        return result

    def __str__(self):
        return "{\n\"name\": " + self.name + \
               ",\n\"teacher\": " + self.teacher + \
                ",\n\"week\": " + str(self.get_times()) + \
                ",\n\"room\": " + self.room + \
                ",\n\"type\": " + self.type + "\n}"

