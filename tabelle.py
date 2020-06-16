import tables
from tkinter import *
from tkinter import ttk
from math import sin
from time import time_ns
from apscheduler.schedulers.background import BackgroundScheduler
from tkinter.font import Font

TABLES = tables.load_tables("tables.json")
QUERY_TABLES = []
BUTTONS = []

sched = BackgroundScheduler()


class Table:

    def __init__(self, root, entries):
        self.frame = Frame(root)

        rows, cols = len(entries), len(entries[0])

        def color(r):
            return 'blue' if r in [0, 1] else entries[i][-1]

        def style(r):
            return 'bold' if r == 0 else 'italic'

        for i in range(rows):
            for j in range(cols):
                self.e = Entry(self.frame, width=12, fg=color(i), font=('Segoe UI', 10, style(i)))
                self.e.grid(row=i, column=j)
                self.e.insert(END, entries[i][j])

    def pack(self, **args):
        self.frame.pack(args)

    def place(self, **args):
        self.frame.place(args)

    def destroy(self):
        self.frame.destroy()


def get_field(id):
    fields = tables.load_fields_from_json('table_fields.json')
    return fields[id]


def table_from_1d(root, result):
    table_entries = [list(result.row), [get_field(id).unit for id in list(result.row)]]

    if result.exact:
        table_entries.append([result.row[col] for col in table_entries[0]] + ['red'])
    else:
        table_entries.append([result.low_row[col] for col in table_entries[0]] + ['black'])
        table_entries.append([result.row[col] for col in table_entries[0]] + ['red'])
        table_entries.append([result.hi_row[col] for col in table_entries[0]] + ['black'])

    table = Table(root, table_entries)
    QUERY_TABLES.append(table)
    return table


def table_from_2d(root, result):
    table_entries = [list(result.row), [get_field(id).unit for id in list(result.row)]]

    table_entries.append([result.row[col] for col in table_entries[0]] + ['red'])

    if result.row_00 != None:
        table_entries.append([result.row[col] for col in table_entries[0]] + ['blue'])

    if result.row_01 != None:
        table_entries.append([result.row_01[col] for col in table_entries[0]] + ['blue'])

    if result.row_10 != None:
        table_entries.append([result.row_10[col] for col in table_entries[0]] + ['blue'])

    if result.row_11 != None:
        table_entries.append([result.row_11[col] for col in table_entries[0]] + ['blue'])

    table = Table(root, table_entries)
    QUERY_TABLES.append(table)
    return table


def table_from_quality(root, result_qlt):
    table_entries2 = [list(result_qlt.groups), [get_field(id).unit for id in list(result_qlt.groups)]]
    table_entries2.append([result_qlt.groups[col] for col in table_entries2[0]] + ['red'])
    table2 = Table(root, table_entries2)
    QUERY_TABLES.append(table2)

    return table2


def clear_buttons():
    for b in BUTTONS:
        b.destroy()


def clear_queries():
    for qt in QUERY_TABLES:
        qt.destroy()

    QUERY_TABLES.clear()


def init_1d_buttons(root, selected):
    clear_queries()
    clear_buttons()

    def query():
        clear_queries()

        frame = Frame(root)

        result = TABLES[selected]['object'].query_table_1d((var1.get(), float(value1.get())))
        table = table_from_1d(frame, result)
        table.pack(side=TOP, fill=X, pady=10)

        try:
            result_qlt = TABLES[selected]["object"].query_table_1d_qlt(result.row, (var2.get(), float(value2.get())))

            table = table_from_quality(frame, result_qlt)
            table.pack(side=TOP, fill=X, pady=10)
        except Exception as ex:
            pass

        frame.place(x=10, y=200)

    fields = TABLES[selected]['fields']
    groups = list(TABLES[selected]['object']._groups.keys())

    var1 = StringVar(value=fields[0])
    var2 = StringVar(value=groups[0])
    unit1 = StringVar(value=get_field(var1.get()).unit)
    unit2 = StringVar(value=get_field(var2.get()).unit)

    def update_unit(eventObject):
        unit1.set(get_field(var1.get()).unit)
        unit2.set(get_field(var2.get()).unit)

    unit_label1 = Label(root, textvariable=unit1)
    unit_label1.place(x=240, y=40)

    unit_label2 = Label(root, textvariable=unit2)
    unit_label2.place(x=240, y=80)

    value1, value2 = StringVar(), StringVar()

    txt1 = Entry(root, width=15, textvariable=value1)
    txt1.place(x=20, y=40)

    cbox1 = ttk.Combobox(root, values=fields, width=10, textvariable=var1)
    cbox1.bind("<<ComboboxSelected>>", update_unit)
    cbox1.place(x=150, y=40)

    txt2 = Entry(root, width=15, textvariable=value2)
    txt2.place(x=20, y=90)

    cbox2 = ttk.Combobox(root, values=groups, width=10, textvariable=var2)
    cbox2.place(x=150, y=90)
    cbox2.bind("<<ComboboxSelected>>", update_unit)

    label1 = Label(root, text='Value from table')
    label2 = Label(root, text='Intermediate value (optional)')

    label1.place(x=20, y=15)
    label2.place(x=20, y=65)

    button = Button(text='Qwuwery OwO', command=query, fg='black', width=15,
                    height=1, font=Font(family='Comic Sans MS', weight='bold', size=20))
    button.place(x=20, y=120)

    def color_changer():
        try:
            button.configure(bg=makeColorGradient(time_ns() / 10e8 * 2, center=180, width=75))
        except Exception:
            pass

    sched.add_job(color_changer, 'interval', seconds=0.05)

    BUTTONS.extend([unit_label1, unit_label2, txt1, txt2, cbox1, cbox2, button, label1, label2])


def init_2d_buttons(root, selected):
    clear_queries()
    clear_buttons()

    def query():
        clear_queries()

        frame = Frame(root)

        result = TABLES[selected]['object'].query_table_2d(
            (var1.get(), float(value1.get())), (var2.get(), float(value2.get())))
        table = table_from_2d(frame, result)
        table.pack(side=TOP, fill=X, pady=10)

        frame.place(x=10, y=200)

    fields = TABLES[selected]['fields']
    groups = TABLES[selected]['fields']

    var1 = StringVar(value=fields[0])
    var2 = StringVar(value=groups[0])
    unit1 = StringVar(value=get_field(var1.get()).unit)
    unit2 = StringVar(value=get_field(var2.get()).unit)

    def update_unit(eventObject):
        unit1.set(get_field(var1.get()).unit)
        unit2.set(get_field(var2.get()).unit)

    unit_label1 = Label(root, textvariable=unit1)
    unit_label1.place(x=240, y=40)

    unit_label2 = Label(root, textvariable=unit2)
    unit_label2.place(x=240, y=80)

    value1, value2 = StringVar(), StringVar()

    txt1 = Entry(root, width=15, textvariable=value1)
    txt1.place(x=20, y=40)

    cbox1 = ttk.Combobox(root, values=fields, width=10, textvariable=var1)
    cbox1.bind("<<ComboboxSelected>>", update_unit)
    cbox1.place(x=150, y=40)

    txt2 = Entry(root, width=15, textvariable=value2)
    txt2.place(x=20, y=90)

    cbox2 = ttk.Combobox(root, values=groups, width=10, textvariable=var2)
    cbox2.place(x=150, y=90)
    cbox2.bind("<<ComboboxSelected>>", update_unit)

    button = Button(text='Query!', command=query)
    button.place(x=20, y=120)

    label1 = Label(root, text='First value from table')
    label2 = Label(root, text='Second value from table')

    label1.place(x=20, y=15)
    label2.place(x=20, y=65)

    BUTTONS.extend([unit_label1, unit_label2, txt1, txt2, cbox1, cbox2, button, label1, label2])


def main():
    root = Tk()
    root.geometry('1000x600')

    selectedTable = StringVar()

    query_tables = []

    def load_buttons(eventObject=None):
        if TABLES[selectedTable.get()]['dimensions'] == 1:
            init_1d_buttons(root, selectedTable.get())
        else:
            init_2d_buttons(root, selectedTable.get())

    options = list(TABLES.keys())

    combo = ttk.Combobox(root, values=options, width=50, textvariable=selectedTable, state='readonly')
    combo.bind("<<ComboboxSelected>>", load_buttons)

    combo.set(options[0])
    combo.pack(padx=5, pady=5)
    load_buttons()

    def on_closing():
        sched.shutdown(wait=True)
        exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    sched.start()
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
    # resp1 = TABLES[0]["object"].query_table_1d(("P_sat_bar", 0.95))
    # print(resp1)
    # # # 2 - Usando quella riga fai una query fornendo una grandezza tra "h", "l", "s", "u", "x"
    # print(TABLES[0]["object"].query_table_1d_qlt(resp1.row, ("x", 0.5)))


def makeColorGradient(freq, phase1=0, phase2=2, phase3=4, center=128, width=127):
    r = sin(freq + phase1) * width + center
    g = sin(freq + phase2) * width + center
    b = sin(freq + phase3) * width + center

    def to_string(val):
        return str(hex(int(val)))[2:].rjust(2, '0')

    return f'#{to_string(r)}{to_string(g)}{to_string(b)}'


if __name__ == "__main__":
    main()
