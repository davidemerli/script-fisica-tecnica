import tables
from tkinter import *
from tkinter import ttk

TABLES = tables.load_tables("tables.json")


class Table:

    def __init__(self, root, entries):
        self.frame = Frame(root)

        rows, cols = len(entries), len(entries[0]) - 1

        def color(r):
            return 'blue' if r == 0 else entries[i][-1]

        def style(r):
            return 'bold' if r == 0 else 'italic'

        for i in range(rows):
            for j in range(cols):
                self.e = Entry(self.frame, width=8, fg=color(i), font=('Segoe UI', 10, style(i)))
                self.e.grid(row=i, column=j)
                self.e.insert(END, entries[i][j])

    def pack(self, side):
        self.frame.pack(side=side)

    def destroy(self):
        self.frame.destroy()


def table_from_1d(root, result):
    table_entries = [list(result.row)]

    table_entries.append([result.low_row[col] for col in table_entries[0]] + ['black'])
    table_entries.append([result.row[col] for col in table_entries[0]] + ['red'])
    table_entries.append([result.hi_row[col] for col in table_entries[0]] + ['black'])

    table = Table(root, table_entries)
    return table


def main():
    root = Tk()
    root.geometry('900x600')

    selectedTable = StringVar()

    query_tables = []

    def load_buttons():
        for qt in query_tables:
            qt.destroy()

        query_tables.clear()

        def query():
            result = TABLES[0]["object"].query_table_1d((var1.get(), float(value1.get())))
            table = table_from_1d(root, result)
            query_tables.append(table)
            table.pack(side=LEFT)

            # print(TABLES[0]["object"].query_table_1d_qlt(result.row, (var2.get(), float(value2.get()))))

        var1, var2 = StringVar(), StringVar()
        value1, value2 = StringVar(), StringVar()

        txt1 = Entry(root, width=15, textvariable=value1)
        txt1.place(x=20, y=40)
        cbox1 = ttk.Combobox(root, values=TABLES[0]['fields'], textvariable=var1)
        cbox1.place(x=150, y=40)
        txt2 = Entry(root, width=15, textvariable=value2)
        txt2.place(x=20, y=80)
        cbox2 = ttk.Combobox(root, values=TABLES[0]['fields'], textvariable=var2)
        cbox2.place(x=150, y=80)
        button = Button(text='Query!', command=query)
        button.place(x=20, y=120)

    options = ['Tabella Saturazione Acqua(Pressioni)',
               'Tabella Saturazione Acqua(Temperature)',
               'Tabella Saturazione R134A(Pressioni)',
               'Tabella Saturazione R134A(Temperature)',
               'Tabella Vapore Surriscaldato Acqua',
               'Tabella Vapore Surriscaldato R134a']

    combo = ttk.Combobox(root, values=options, width=50, textvariable=selectedTable,
                         state='readonly', postcommand=load_buttons)
    combo.set("Tabella da interrogare...")
    combo.pack(padx=5, pady=5)

    result = TABLES[0]["object"].query_table_1d(("P_sat_bar", 0.95))

    # table2 = Table(root, table_entries)
    # table2.pack('left')

    # query_tables.extend([table, table2])

    print(TABLES[4]["object"].query_table_2d(("T", 320), ("P_bar", 5.5)))

    root.mainloop()
    # # fields_ids = ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]
    # # water_sat_p = read_form("Tabelle_Acqua_Fix.txt", fields_ids, start=5, end=84)
    # # water_sat_p.print_response(water_sat_p.query_table_1d(("P_sat_bar", 146.0)))
    # # parser = argparse.ArgumentParser(description="Read data from Fisica Tecnica per Informatici tables")
    # # parser.add_argument("sost")
    # # print(TABLES[0]["object"]._groups)
    # # ESEMPIO Query di vapore saturo (Necessita di due parametri indipedenti)
    # print(TABLES[4]["object"].query_table_2d(("T", 320), ("P_bar", 5.5)))
    # # ESEMPIO Query con quality
    # # 1 - Fai una normale query nella tabella di saturazione
    resp1 = TABLES[0]["object"].query_table_1d(("P_sat_bar", 0.95))
    print(resp1)
    # # 2 - Usando quella riga fai una query fornendo una grandezza tra "h", "l", "s", "u", "x"
    print(TABLES[0]["object"].query_table_1d_qlt(resp1.row, ("x", 0.5)))


if __name__ == "__main__":
    main()
