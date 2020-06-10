from collections import namedtuple
import argparse

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


class table1D:
    
    def __init__(self,items : list):
        self._row_metadata = items
        self._entries = [] 
        self._fields_info = dict() #Contains the row headers
        self._fields = []   #Contains all the fields
        for item in items:
            self._fields += item.fields
            self._fields_info[item.name] = item
    
    def add_rows(self,rows : list):
        for row in rows:
            self.add_row(row)

    def add_row(self,row_string : str):
        row_arr = row_string.strip("\n").split(",") #Get array from csv
        if len(row_arr) != len(self._fields):
            print(row_arr)
            print(self._fields)
            raise ValueError("Wrong number of items")
        num_row_arr = list(map(lambda x : float(x), row_arr))  #Convert to float
        row_dict = dict(zip(self._fields,row_arr))
        self._entries.append(row_dict) #Add entry
    
    def print_row(self,row):
        for key,value in self._fields_info:
            print("%s: %f %s" % (value.name, row[value.name], value.unit))
        
    def get_row_field(self, field_name : str, value : float):
        sorted_fields = list(sorted(self._entries,key=lambda x : x[field_name])) #Sort
        hit, rows = table1D.ordered_search(sorted_fields, value, key=lambda x : x[field_name])
        if hit:
            return rows
        low_row, high_row = rows[0], rows[1]
        qlt = calculate_quality(low_row,high_row,value,key=lambda x : x[field_name])
        return interpolate_rows(low_row,high_row,key=lambda x : x[field_name])

    @classmethod
    def ordered_search(cls, array, item, key):
        low_idx = None
        for i, row in enumerate(array):
            if float_equals(key(row), item):
                return True, row
            if float_greater_than(key(row), item):
                low_idx = None
                break
        if low_idx == 0:
            raise ValueError("Out of table range")
        low_row = array[low_idx]
        hi_row = array[hi_idx - 1]
        return False, (low_row, hi_idx)
    
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
        mid_row = dict()
        for col in low_row.keys:
            mid_row[col] = low_row[col]*(1-quality) + hi_row[col]*quality
        return mid_row

    @classmethod
    def float_equals(cls, f1 : float,f2 :float):
        return abs(f1 - f2) < EPS

    @classmethod
    def float_greater_than(cls, f1 : float, f2 : float):
        return f1 - f2 > EPS
    
def read_form(file_name : str, order_list : list,start=0,end=None):
    with open(file_name, "r") as table:
        lines = None
        if(end != None):
            lines = table.readlines()[start:end]
        else:
            lines = table.readlines()[start:]
        table = table1D(order_list)
        table.add_rows(lines)
        return table

def main():
    water_sat_T = read_form("Tabelle_Acqua_Fix.txt",[Tsat,Psat_bar,v,h,s],start=5,end=84)
    water_sat_T.print_row(water_sat_T.get_row_field("Tsat",150.0))
    #parser = argparse.ArgumentParser(description="Read data from Fisica Tecnica per Informatici tables")
    #parser.add_argument("sost")

if __name__ == "__main__":
    main()

