import re
from srl import SRL


def learn(strings):
    overall = filter(search_overall(strings))
    never = search_never(strings, overall)
    oppor = group_opport(strings, overall, never)
    return translate(oppor)


def search_overall(strings):
    overall = []
    for i in range(len(strings)):
        s = strings[i]
        for k in range(i + 1, len(strings)):
            t = strings[k]
            overall.extend(scan(s, t))

    return overall


def scan(first, second):
    return []


def filter(overall):
    return overall


def search_never(strings, overall):
    return []


def group_opport(strings, overall, never):
    return (("еж",), (["чет", "неч"], "/нед"))


def translate(oppor):
    return "lol"


reg = learn(["еж", "чет/нед", "неч/нед"])

print(re.search(reg, "ММСС, пр, Парамонов, чет/нед, ДМ, 4-16н, а.512/1"))
print(re.search(reg, "Физическая культура, пр, еж, 2-18н, 18н-зачет, спортзал"))
print(re.search(reg, "ММСС, лаб, Парамонов, неч/нед, 3-17н, а.508/1"))
