from ValuesTable import ValuesTable
from collections import namedtuple
import json
from functools import lru_cache
import sympy as sym

sym.init_printing()

x = sym.symbols('x')

EPS = 0.00001
field = namedtuple("field", ["id", "name", "description", "group", "unit", "decimals"])


def read_1d(file_name: str, order_list: list, start=0, end=None):
    with open(file_name, "r") as table:
        if end is not None:
            lines = table.readlines()[start:end]
        else:
            lines = table.readlines()[start:]
        table = ValuesTable(fields_ids=order_list)
        table.add_rows(lines)
        return table


def read_2d(file_name: str, order_list: list, ranges: list):
    with open(file_name, "r") as data:
        v_table = ValuesTable(fields_ids=order_list)
        lines = data.readlines()
        for r in ranges:
            start, end = r["start"], r["end"]
            pressure = lines[start]
            for i in range(start + 1, end):
                v_table.add_row("%s,%s" % (pressure.strip("\n"), lines[i]))
        return v_table


def load_tables(file_name: str):
    with open(file_name, "r") as data:
        tables_list = json.loads(data.read())
        for table in tables_list:
            if table["dimensions"] == 1:
                table["object"] = read_1d(table["filename"], table["fields"], start=table["start"], end=table["end"])
            elif table["dimensions"] == 2:
                table["object"] = read_2d(table["filename"], table["fields"], table["ranges"])
            else:
                raise ValueError("Bruh, le interpolazioni trilineari non sono disponibili")
            print("%s loaded" % table["name"])
        return {table["name"]: table for table in tables_list}


@lru_cache
def load_fields_from_json(filename: str):
    with open(filename, "r") as j_file:
        j_string = j_file.read()
        j_array = json.loads(j_string)
        return dict(map(lambda item: (item["id"], field(**item)), j_array))


def ordered_search(array, item, key=lambda y: y):
    hi_idx = 0
    for i, row in enumerate(array):
        if float_equals(key(row), item):
            return True, row
        if float_greater_than(key(row), item):
            hi_idx = i
            break
    if hi_idx == 0:
        raise ValueError("Out of table range")
    hi_row = array[hi_idx]
    low_row = array[hi_idx - 1]
    return False, (low_row, hi_row)


def calculate_quality(low_row, hi_row, value, key=lambda x: x):
    low_value = min(key(low_row), key(hi_row))
    hi_value = max(key(low_row), key(hi_row))
    if not (low_value < value < hi_value):
        print("LOW:%f CURR:%f HI:%f" % (low_value, value, hi_value))
        raise ValueError("Interpolation out of range")
    qlt = (value - low_value) / (hi_value - low_value)

    print(f'x = ({value} - {low_value}) / ({hi_value} - {low_value})')

    return qlt


def interpolate_rows(low_row, hi_row, quality):
    mid_row = dict()
    for col in low_row.keys():
        print(f'{col} = {low_row[col]} * (1 - {quality}) + {hi_row[col]} * {quality}', end='\n\n')

        mid_row[col] = low_row[col] * (1 - quality) + hi_row[col] * quality

    return mid_row


def float_equals(f1: float, f2: float):
    return abs(f1 - f2) < EPS


def float_greater_than(f1: float, f2: float):
    return f1 - f2 > EPS
