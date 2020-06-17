import tables
from urllib.request import urlopen
from tkinter import *
from tkinter import ttk
from math import sin
from time import time_ns, sleep
from tkinter.font import Font
from threading import Thread
import json

VERSION_LINK = 'https://raw.githubusercontent.com/davidemerli/script-fisica-tecnica/master/version.json'

TABLES = tables.load_tables("tables.json")
QUERY_TABLES = []
BUTTONS = []


class Table:

    def __init__(self, root, entries):
        self.frame = Frame(root)
        self.frame.configure(bg='#325985')

        rows, cols = len(entries), len(entries[0])

        def color(r):
            return 'blue' if r in [0, 1] else entries[i][-1]

        def style(r):
            return 'bold' if r == 0 or entries[i][-1] == 'red' else 'italic'

        for i in range(rows):
            for j in range(cols):
                self.e = Entry(self.frame, width=10, fg=color(i), font=('Consolas', 11, style(i)))
                self.e.configure(background='#A7BFDD')
                self.e.grid(row=i, column=j)
                self.e.insert(END, entries[i][j])
                self.e.configure(state='readonly')

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
    print(result)
    table_entries = [list(result.row), [get_field(id).unit for id in list(result.row)]]

    table_entries.append([result.row[col] for col in table_entries[0]] + ['red'])

    if result.row_00 is not None:
        table_entries.append([result.row_00[col] for col in table_entries[0]] + ['blue'])

    if result.row_01 is not None:
        table_entries.append([result.row_01[col] for col in table_entries[0]] + ['blue'])

    if result.row_10 is not None:
        table_entries.append([result.row_10[col] for col in table_entries[0]] + ['blue'])

    if result.row_11 is not None:
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
        frame.configure(bg='#325985')

        result = None

        try:
            result = TABLES[selected]['object'].query_table_1d((var1.get(), float(value1.get())))

            table = table_from_1d(frame, result)
            table.pack(anchor=CENTER, padx=10, pady=10)
        except Exception as ex:
            exception = Label(frame, text=ex.with_traceback(None), fg='red')
            exception.pack(side=BOTTOM)

        try:
            if result != None:
                result_qlt = TABLES[selected]["object"].query_table_1d_qlt(
                    result.row, (var2.get(), float(value2.get())))

                table = table_from_quality(frame, result_qlt)
                table.pack(anchor=CENTER, padx=10, pady=10)
        except Exception as ex:
            exception = Label(frame, text=ex.with_traceback(None), fg='red')
            exception.pack(side=BOTTOM)

        frame.place(relx=0.5, y=350, anchor=CENTER)
        BUTTONS.append(frame)

    fields = TABLES[selected]['fields']
    groups = list(TABLES[selected]['object']._groups.keys())
    groups.append("x")

    var1 = StringVar(value=fields[0])
    var2 = StringVar(value=groups[0])
    unit1 = StringVar(value=get_field(var1.get()).unit)
    unit2 = StringVar(value=get_field(var2.get()).unit)

    def update_unit(eventObject):
        unit1.set(get_field(var1.get()).unit)
        unit2.set(get_field(var2.get()).unit)

    unit_label1 = Label(root, textvariable=unit1, fg='#A7BFDD', bg='#2D3142', font=('Consolas', 12, 'bold'))
    unit_label1.place(x=350, y=40)

    unit_label2 = Label(root, textvariable=unit2, fg='#A7BFDD', bg='#2D3142', font=('Consolas', 12, 'bold'))
    unit_label2.place(x=350, y=90)

    value1, value2 = StringVar(), StringVar()

    txt1 = Entry(root, width=15, textvariable=value1, fg='#F7DEE0', bg='#D1495B', font=('Consolas', 12, 'bold'))
    txt1.place(x=20, y=40)

    cbox1 = ttk.Combobox(root, values=fields, width=10, textvariable=var1,
                         state='readonly', font=('Consolas', 12, 'bold'))
    cbox1.bind("<<ComboboxSelected>>", update_unit)
    cbox1.place(x=200, y=40)

    txt2 = Entry(root, width=15, textvariable=value2, fg='#F7DEE0', bg='#D1495B', font=('Consolas', 12, 'bold'))
    txt2.place(x=20, y=100)

    cbox2 = ttk.Combobox(root, values=groups, width=10, textvariable=var2,
                         state='readonly', font=('Consolas', 12, 'bold'))
    cbox2.place(x=200, y=100)
    cbox2.bind("<<ComboboxSelected>>", update_unit)

    label1 = Label(root, text='Value from table', fg='white', bg='#2D3142', font=('Consolas', 12, 'bold'))
    label2 = Label(root, text='Intermediate value (optional)', fg='white', bg='#2D3142', font=('Consolas', 12, 'bold'))

    label1.place(x=20, y=15)
    label2.place(x=20, y=75)

    button = Button(text='Query!', command=query, fg='black', width=15,
                    height=1, font=Font(family='Consolas', weight='bold', size=20))
    button.place(x=20, y=140)

    def color_changer():
        while True:
            sleep(0.01)
            button.configure(bg=makeColorGradient(time_ns() / 10e8 * 2, center=180, width=75))

    Thread(target=color_changer).start()

    BUTTONS.extend([unit_label1, unit_label2, txt1, txt2, cbox1, cbox2, button, label1, label2])


def init_2d_buttons(root, selected):
    clear_queries()
    clear_buttons()

    def query():
        clear_queries()

        frame = Frame(root)
        frame.configure(bg='#325985')

        v1, v2 = (var1.get(), float(value1.get())), (var2.get(), float(value2.get()))

        try:
            result = TABLES[selected]['object'].query_table_2d(v1, v2)
            table = table_from_2d(frame, result)
            table.pack(anchor=CENTER, padx=10, pady=10)
        except Exception as ex:
            exception = Label(frame, text=ex.with_traceback(None), fg='red')
            exception.pack(side=BOTTOM)

        frame.place(relx=0.5, y=300, anchor=CENTER)
        BUTTONS.append(frame)

    fields = TABLES[selected]['fields']
    groups = TABLES[selected]['fields']

    var1 = StringVar(value=fields[0])
    var2 = StringVar(value=groups[0])
    unit1 = StringVar(value=get_field(var1.get()).unit)
    unit2 = StringVar(value=get_field(var2.get()).unit)

    def update_unit(eventObject):
        unit1.set(get_field(var1.get()).unit)
        unit2.set(get_field(var2.get()).unit)

    unit_label1 = Label(root, textvariable=unit1, fg='#A7BFDD', bg='#2D3142', font=('Consolas', 12, 'bold'))
    unit_label1.place(x=350, y=40)

    unit_label2 = Label(root, textvariable=unit2, fg='#A7BFDD', bg='#2D3142', font=('Consolas', 12, 'bold'))
    unit_label2.place(x=350, y=90)

    value1, value2 = StringVar(), StringVar()

    txt1 = Entry(root, width=15, textvariable=value1, fg='#F7DEE0', bg='#D1495B', font=('Consolas', 12, 'bold'))
    txt1.place(x=20, y=40)

    cbox1 = ttk.Combobox(root, values=fields, width=10, textvariable=var1,
                         state='readonly', font=('Consolas', 12, 'bold'))
    cbox1.bind("<<ComboboxSelected>>", update_unit)
    cbox1.place(x=200, y=40)

    txt2 = Entry(root, width=15, textvariable=value2, fg='#F7DEE0', bg='#D1495B', font=('Consolas', 12, 'bold'))
    txt2.place(x=20, y=100)

    cbox2 = ttk.Combobox(root, values=groups, width=10, textvariable=var2,
                         state='readonly', font=('Consolas', 12, 'bold'))
    cbox2.place(x=200, y=100)
    cbox2.bind("<<ComboboxSelected>>", update_unit)

    label1 = Label(root, text='First value from table', fg='white', bg='#2D3142', font=('Consolas', 12, 'bold'))
    label2 = Label(root, text='Second value from table', fg='white', bg='#2D3142', font=('Consolas', 12, 'bold'))

    label1.place(x=20, y=15)
    label2.place(x=20, y=75)

    button = Button(text='Query!', command=query, fg='black', width=15,
                    height=1, font=Font(family='Consolas', weight='bold', size=20))
    button.place(x=20, y=140)

    def color_changer():
        while True:
            sleep(0.01)

            button.configure(bg=makeColorGradient(time_ns() / 10e8 * 2, center=180, width=75))

    Thread(target=color_changer).start()

    BUTTONS.extend([unit_label1, unit_label2, txt1, txt2, cbox1, cbox2, button, label1, label2])


def main():
    root = Tk()
    root.geometry('1200x600')
    root.configure(background='#2D3142')

    with open('version.json', 'r') as version_file:
        version = json.load(version_file)['version']
        root.title(f'Fisica Tecninator 4200 v {version}')

        online_version = json.load(urlopen(VERSION_LINK))['version']

        if version < online_version:
            label = Label(root, text=f'This (v{version}) is not the newest version({online_version})!')
            label.configure(fontsize='20', fg='red')
            label.pack(side=RIGHT)

    selectedTable = StringVar()

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
        exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def makeColorGradient(freq, phase1=0, phase2=2, phase3=4, center=128, width=127):
    r = sin(freq + phase1) * width + center
    g = sin(freq + phase2) * width + center
    b = sin(freq + phase3) * width + center

    def to_string(val):
        return str(hex(int(val)))[2:].rjust(2, '0')

    return f'#{to_string(r)}{to_string(g)}{to_string(b)}'


if __name__ == "__main__":
    main()
