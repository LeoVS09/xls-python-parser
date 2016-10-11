import re
from srl import SRL



def learn(strings):
    overall = filter(search_overall(strings))
    never = filter(search_never(strings, overall))
    oppor = group_opport(strings, overall, never)
    srl = translate(oppor)
    print(srl)
    return str(srl)


def search_overall(strings):
    overall = []
    for i in range(len(strings)):
        s = strings[i]
        for k in range(i + 1, len(strings)):
            t = strings[k]
            overall.extend(scan(s, t))

    return overall


def scan(first, second):
    result = []
    for f in first:
        for s in second:
            if f == s:
                result.append(f)
    return result


def filter(overall):
    result = []
    for element in overall:
        if element not in result:
            result.append(element)
    return result


def search_never(strings, overall):
    result = []
    for string in strings:
        for s in string:
            if s not in overall:
               result.append(s)
    return result


def group_opport(strings, overall, never):
    result = []
    for i in range(len(strings)):
        string = strings[i]
        br = []
        ar = ""
        for s in string:
            if s in overall:
                ar += s
            elif ar != "":
                br.append(ar)
                ar = ""
        if len(br) == 0:
            result.append((string,))
        else:
            br.sort(key=lambda el: len(el),reverse=True)
            ar = br[0]
            searched = False
            for k in range(i+1,len(strings)):
                other = strings[k]
                find_other = other.find(ar)
                if find_other != -1:

                    find_string = string.find(ar)
                    if find_other != 0 and find_string != 0:
                        first = [string[:find_string],other[:find_other]]
                    elif find_other == 0 and find_string == 0:
                        first = False
                    else:
                        first = string[:find_string] if find_other == 0 else other[:find_other]
                    if find_other != len(other)-1 and find_string != len(string)-1:
                        second = [string[find_string + len(ar):], other[find_other + len(ar):]]
                    elif find_other == len(other)-1 and find_string == len(string)-1:
                        second = False
                    else:
                        second = string[find_string + len(ar):] if find_other == len(other)-1 else other[find_other + len(ar):]
                    if first and second:
                        result.append((first,ar,second))
                    elif not first and not second:
                        result.append(ar)
                    elif first:
                        result.append((first,ar))
                    else:
                        result.append((ar,second))
                    searched = True
            if not searched:
                result.append((string,))

    print(result)
    return result #(("еж",), (["чет", "неч"], "/нед"))


def translate(oppor):

    result = "any of ("
    for variant in oppor:
        result += "( "
        if len(variant) == 1:
            result += "literally \"" + variant[0] + "\"),"
        else:
            for v in variant:
                if type(v) is list:
                    result += "any of ("
                    for element in v:
                        result += "literally \"" + element + "\","
                    result = result[:-1]
                    result += "),"
                else:
                    result += "literally \"" + v + "\","
            result = result[:-1] + "),"

    result = result[:-1]
    result += ")"
    return srl_capture(result)

def srl_capture(string):
    string = "capture (" + string + ")"
    print(string)
    return SRL(string)


reg = learn(["еж", "чет/нед", "неч/нед"])

print(re.search(reg, "ММСС, пр, Парамонов, чет/нед, ДМ, 4-16н, а.512/1"))
print(re.search(reg, "Физическая культура, пр, еж, 2-18н, 18н-зачет, спортзал"))
print(re.search(reg, "ММСС, лаб, Парамонов, неч/нед, 3-17н, а.508/1"))
