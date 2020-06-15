from table1D import table1D
from tables import load_fields_from_json

TABLES = {'Tabelle Acqua': ['Tabelle_Acqua_Fix.txt', (5, 84), ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]],
            # 'Tabelle Aria': ['Tabelle_Aria_Fix.txt', (5, 65), ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]],
            'Tabelle R134': ['Tabelle_R134a_Fix.txt', (5, 65), ["T_sat", "P_sat_MPa", "v_l", "dv", "v_v", "u_l", "u_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]]}
   
def read_from(file_name: str, order_list: list, start=0, end=None):
    with open(file_name, "r") as table:
        lines = None
        if end is not None:
            lines = table.readlines()[start:end]
        else:
            lines = table.readlines()[start:]
        table = table1D(fields_ids=order_list)
        table.add_rows(lines)
        return table

def print_intro():
    print("TABLES:")

    for i, t in enumerate(TABLES.keys()):
        print(f'{i + 1}) {t}', end='\t')
    print('\n')

    print("Please choose which table (index) you want to get data from: ", end='')


def print_query_choices(headers):
    dict_ = load_fields_from_json('table_fields.json')

    print("QUANTITIES:")

    for i, h in enumerate(headers):
        print(f'{i + 1}) {dict_[h][1]}   \t {dict_[h][2]}')
    print()

    print("Please choose which quantity you want to query with: ", end='')

def main():
    while True:
        print_intro()
        choice = int(input())

        table = TABLES[list(TABLES.keys())[choice - 1]]

        headers = table[2]
        print_query_choices(table[2])
        
        table = read_from(table[0], headers, start=table[1][0], end=table[1][1])

        choice = headers[int(input()) - 1]

        print("Please insert value: ", end='')
        value = float(input())

        query = table.query_table(choice, value)
        table.print_response(query)


if __name__ == "__main__":
    main()
