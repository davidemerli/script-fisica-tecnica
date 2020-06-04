from collections import namedtuple

entry = namedtuple("entry",["name","fields","description","unit"])
#Order list items
Tsat = entry("Tsat",["Tsat"],"Temperatura di saturazione","°C")
Psat_bar = entry("Psat",["Psat"],"Temperatura di saturazione","bar")
Psat_Mpa = entry("Psat",["Psat"],"Temperatura di saturazione","MPa")
h = entry("h",["h_l","dh","h_v"],"Entalpia Specifica","kJ/kg")
v = entry("v",["v_l","dv","v_v"],"Volume Specifico","m^3/kg")
s = entry("s",["s_l","ds","s_v"],"Entropia Specifica","kJ/kgK")
u = entry("u",["u_l","u_v"],"Energia Interna specifica","kJ/kgK")
EPS = 0.00001


class table():
    
    def __init__(self,fields : list[str]):
        self._row_type = namedtuple("rows",fields)
        self._entries = [] 
        self._fields = fields

    def add_row(self,row_string : str):
        row_arr = row_string.split(",")
        if len(row_arr) != self._fields:
            raise ValueError("Wrong number of items")
        num_row_arr = list(map(lambda x : float(x), num_row_arr))
        self._entries.add(self._row_type(*num_row_arr))
        
    def get_row_field(self, field_name : str, value : float):
        sorted_fields = list(sorted(self._entries,key=lambda x : getattr(x,field_name)))

    
    @classmethod #TODO: hi_idx undefined
    def ordered_search(cls, array, item, key, quality=None):
        low_idx = None
        for i, row in enumerate(array):
            if float_equals(key(row), item):
                return True, row
            if float_greater_than(key(row), item):
                low_idx = None
                break
        if low_idx == 0:
            raise ValueError("Out of table range")
        low_row = array[hi_idx]
        hi_row = array[hi_idx - 1]
    
    @classmethod
    def calculate_quality(cls, low_row, hi_row, value, key):
        low_value = min(key(low_row),key(hi_row))
        hi_value = max(key(low_row),key(hi_row))
        if low_value < value and value < hi_value:
            raise ValueError("Interpolation out of range")
        qlt = (value - low_value)/(hi_value - low_value)
        return qlt


    @classmethod
    def interpolate_rows(cls, low_row, hi_row, quality):
        pass

    @classmethod
    def float_equals(cls, f1 : float,f2 :float):
        return abs(f1 - f2) < EPS

    @classmethod
    def float_greater_than(cls, f1 : float, f2 : float):
        return f1 - f2 > EPS



def read_form(file_name, order_list):
    with table as open(file_name, "r"):
        pass
        


