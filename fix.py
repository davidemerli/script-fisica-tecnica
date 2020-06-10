def fix_acqua():
    lines = open('Tabelle_Acqua.txt').readlines()

    counter = 0

    for i, l in enumerate(lines):
        if i < 179 or i > len(lines) - 2:
            continue
        # print(i, l.split('\t'))

        split = l.split('\t')

        values = split[1].split(',')

        if len(values) > counter:
            counter = len(values)

        new_vals = ['-' for _ in range(counter - len(values))]
        new_vals.extend(values)
        split[1] = (','.join(new_vals))

        lines[i] = '\t'.join(split)

        print(lines[i])

    for l in lines:
        print(l)

    open('Tabelle_Acqua_Fix.txt', 'w').writelines(lines)

tabs = []

def fix_r134():
    lines = open('Tabelle_R134a.txt').readlines()

    current1, current2, current3 = [], [], []

    for i, l in enumerate(lines):
        if i < 140: continue
        l = l.strip()
        split, size = l.split(','), len(l.split(','))

        if size > 1:
            line1 = split[:5]
            line2 = split[5:10]
            line3 = split[10:15]

            current1.append(line1)
            current2.append(line2)
            current3.append(line3)

            # print(i, split)
            # print(i, line1, line2)
        else:
            tabs.append(current1)
            tabs.append(current2)
            tabs.append(current3)

            current1, current2, current3 = [], [], []

            
    for tab in tabs:
        print()
        
        for line in tab:
            print(','.join(line))

def fix_water_2():
    lines = [l.strip() for l in open('temp').readlines() if len(l.strip()) != 0]
    temps = lines[1].split('\t')[1].split(',')

    lines = lines[2:]
    new = open('fix_water', 'a')

    print(temps)

    for i in range(0, len(lines), 3):
        p = lines[i + 1].split()[0]

        def get_values(s):
            return s.split('\t')[1].split(',')

        v = get_values(lines[i])
        h = get_values(lines[i + 1])
        s = get_values(lines[i + 2])

        print(p)

        print(v)
        print(h)
        print(s)

        new.write(f'P [bar]\n')
        new.write(f'{p}\n')

        for j in range(len(v)):
            new.write(f'{temps[j]},{v[j]},{h[j]},{s[j]}\n')

        new.write('\n\n')



if __name__ == '__main__':
    fix_water_2()