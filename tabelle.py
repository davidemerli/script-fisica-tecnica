import tables

TABLES = tables.load_tables("tables.json")


def print_intro():
    print("TABLES:")

    for i, t in enumerate(TABLES):
        print(f'{i + 1}) {t["name"]}', end='\n')
    print('\n')

    print("Please choose which table (index) you want to get data from: ", end='')


def print_query_choices(headers):
    dict_ = tables.load_fields_from_json('table_fields.json')

    print("QUANTITIES:")

    for i, h in enumerate(headers):
        print(f'{i + 1}) {dict_[h][1]}   \t {dict_[h][2]}')
    print()

    print("Please choose which quantity you want to query with: ", end='')


def main():
    # fields_ids = ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]
    # water_sat_p = read_form("Tabelle_Acqua_Fix.txt", fields_ids, start=5, end=84)
    # water_sat_p.print_response(water_sat_p.query_table_1d(("P_sat_bar", 146.0)))
    # parser = argparse.ArgumentParser(description="Read data from Fisica Tecnica per Informatici tables")
    # parser.add_argument("sost")
    print(TABLES)
    # ESEMPIO Query di vapore saturo (Necessita di due parametri indipedenti)
    print(TABLES["Tabella Vapore Surriscaldato Acqua"]["object"].query_table_2d(("T", 320), ("P_bar", 5.5)))
    # ESEMPIO Query con quality
    # 1 - Fai una normale query nella tabella di saturazione
    resp1 = TABLES["Tabella Saturazione Acqua (Pressioni)"]["object"].query_table_1d(("P_sat_bar", 0.95))
    print(resp1)
    # 2 - Usando quella riga fai una query fornendo una grandezza tra "h", "l", "s", "u", "x"
    print(TABLES["Tabella Saturazione Acqua (Pressioni)"]["object"].query_table_1d_qlt(resp1.row, ("x", 0.5)))

    while True:
        print_intro()
        choice = int(input())

        # table = TABLES[list(TABLES.keys())[choice - 1]]
        table_data = TABLES[choice - 1]

        headers = table_data["fields"]
        print_query_choices(headers)

        table = table_data["object"]

        choice = headers[int(input()) - 1]

        print("Please insert value: ", end='')
        value = float(input())

        query = table.query_table_1d((choice, value))
        table.print_response(query)


if __name__ == "__main__":
    main()
