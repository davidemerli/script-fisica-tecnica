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

if __name__ == '__main__':
    fix_r134()