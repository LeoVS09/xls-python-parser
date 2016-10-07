import xlrd
import data
from Group import Group


def pair_merged(sheet):

    for merged in sheet.merged_cells:
        rbeg, rend, cbeg, cend = merged
        cell = sheet.cell(rbeg, cbeg)
        for row in range(rbeg, rend):
            for col in range(cbeg, cend):
                sheet.put_cell(row, col, cell.ctype, cell.value, cell.xf_index)


def filter(sheet):

    for rx in range(sh.nrows):
        for cx in range(sh.ncols):
            cell = sh.cell(rx, cx)
            if cell.value in data.without_cells:
                sheet.put_cell(rx, cx, cell.ctype, "", cell.xf_index)


def search_cell(sheet, values):

    result = []
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if sheet.cell(row, col).value in values:
                result.append((row, col))

    return result


def parse_table(sheet):

    groups_row, groups_col = search_cell(sheet, data.GROUPS_IN_TABLE_TITLE)[0]
    last_row, last_col = search_cell(sheet, data.LAST_ROW_TABLE_TITLE)[-1]
    groups = [Group(sheet.cell(groups_row, col).value) for col in range(groups_col + 1, sheet.ncols)]

    i = 0
    for col in range(groups_col + 1, sheet.ncols):
        for row in range(groups_row + 1, last_row):
            groups[i].add_lesson(sheet.cell(row, 0).value, sheet.cell(row, 1).value, sheet.cell(row, col).value)
        i += 1

    return groups


book = xlrd.open_workbook("2.xls", formatting_info=True)
for sh in book.sheets():
    filter(sh)
    pair_merged(sh)
    groups = parse_table(sh)

    for group in groups:
        print(group.name, "------------------------------------------------")
        for name, day in group.days.items():
            print(name, "---", day.name)
            for time, lesson in day.lessons.items():
                for l in lesson:
                    print(time, l)
