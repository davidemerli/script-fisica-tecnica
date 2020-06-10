from table1D import table1D


def read_form(file_name: str, order_list: list, start=0, end=None):
    with open(file_name, "r") as table:
        lines = None
        if end is not None:
            lines = table.readlines()[start:end]
        else:
            lines = table.readlines()[start:]
        table = table1D(fields_ids=order_list)
        table.add_rows(lines)
        return table


def main():
    fields_ids = ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]
    water_sat_p = read_form("Tabelle_Acqua_Fix.txt", fields_ids, start=5, end=84)
    water_sat_p.print_response(water_sat_p.query_table("P_sat_bar", 150.0))
    # parser = argparse.ArgumentParser(description="Read data from Fisica Tecnica per Informatici tables")
    # parser.add_argument("sost")


if __name__ == "__main__":
    main()
