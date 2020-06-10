import tables
from collections import namedtuple
from tabulate import tabulate

response = namedtuple("response", ["field_req", "value_req", "exact", "row", "low_row", "hi_row", "quality"])

class table1D:

    def __init__(self, name: str = "table",
                 fields_ids: list = None, 
                 fields_tuples: list = None, 
                 json_filename: str = "table_fields.json"):

        if (fields_ids is None) == (fields_tuples is None):  # Only on
            # e of two options should be provided
            raise ValueError("Wrong number of optional arguments!")

        self._name = name
        self._entries = []  # List of all rows
        self._fields_info = dict()  # Index of all fields in the table, with all infos
        self._fields = []  # Contains all the fields

        if fields_tuples is not None:
            for item in fields_tuples:
                self._fields.append(item.id)
                self._fields_info[item.id] = item

        if fields_ids is not None:
            fields_dict = tables.load_fields_from_json(json_filename)

            for field_id in fields_ids:
                self._fields.append(fields_dict[field_id].id)
                self._fields_info[field_id] = fields_dict[field_id]

    def add_rows(self, rows: list):
        for row in rows:
            self.add_row(row)

    def add_row(self, row_string: str):
        row_arr = row_string.strip("\n").split(",")  # Get array from csv

        if len(row_arr) != len(self._fields):
            print(row_arr)
            print(self._fields)
            raise ValueError("Wrong number of items")

        num_row_arr = list(map(lambda x: float(x), row_arr))  # Convert to float
        row_dict = dict(zip(self._fields, num_row_arr))  # Create Dictionary with id as keys
        self._entries.append(row_dict)  # Add entry

    def print_row(self, row):
        for field_id in self._fields:
            field = self._fields_info[field_id]
            float_format = "%%s: %%0.%df %%s" % self._fields_info[field_id].decimals  # Format decimal places
            print(float_format % (field.name, row[field_id], field.unit))

    def print_flanked_rows(self, low_row, row, hi_row):
        for field_id in self._fields:
            field = self._fields_info[field_id]
            decimals = self._fields_info[field_id].decimals
            float_format = "%%s: (%%0.%df) - %%0.%df - (%%0.%df) %%s" % (decimals, decimals, decimals)
            print(float_format % (field.name, low_row[field_id], row[field_id], hi_row[field_id], field.unit))

    def print_response(self, q_response):
        print("Requested %s=%f from %s" % (q_response.field_req, q_response.value_req, self._name))
       
        if q_response.exact:
            print("Exact Match Found!")
            # self.print_row(q_response.row)
            print(tabulate([f'\x1b[31m{v}\x1b[0m' for v in q_response.row.values()], headers=list(q_response.row.keys()), tablefmt='fancy_grid'))
        else:
            print("Interpolated result with quality=%f" % q_response.quality)
            # self.print_flanked_rows(q_response.low_row, q_response.row, q_response.hi_row)
            print(tabulate([q_response.low_row.values(), [f'\x1b[31m{v}\x1b[0m' for v in q_response.row.values()], q_response.hi_row.values()], \
                    headers=list(q_response.low_row.keys()), tablefmt='fancy_grid'))

    def query_table(self, field_id: str, value: float):
        sorted_fields = list(sorted(self._entries, key=lambda x: x[field_id]))  # Sort fields for value
        hit, rows = tables.ordered_search(sorted_fields, value, key=lambda x: x[field_id])  # Search for key

        if hit:
            return response(field_id, value, True, rows, None, None, 1.00)  # Exact Match

        # No exact match, need to interpolate
        low_row, high_row = rows[0], rows[1]  # Unpack lower / Higher bound
        qlt = tables.calculate_quality(low_row, high_row, value, key=lambda x: x[field_id])
        mid_row = tables.interpolate_rows(low_row, high_row, qlt)

        return response(field_id, value, False, mid_row, low_row, high_row, qlt)
