

def parse(s):
    """
    format of s: [date] - [start-hr] [end-hr], [start-hr] [end-hr], ... (hrs)
    example:     10.18 - 0.5 3, 7 11, 17.5 19 (8)
    The (8) is optional.
    return ("date", [(start-hr, end-hr), (start-hr, end-hr), ...])
    """
    a = s.split(' - ')
    date = a[0]
    a = a[1].split(', ')
    a[-1] = a[-1].split('(')[0]
    hrs = []
    for _ in a:
        _ = _.split(' ')
        start, end = float(_[0]), float(_[1])
        hrs.append((start, end))
    return date, hrs


def intervals(yrs=(17, 18, 19, 20, 21, 22)):
    """
    Prints the percentage of time I'm asleep for each half-hour interval of the day,
    for selected years
    """
    total_days = 0
    hrs = [0] * 48  # 48 half-hour intervals
    for yr in yrs:
        file = f"diary/sleep_{yr}.txt"
        with open(file) as f:
            for l in f:
                if len(l) < 2:
                    continue
                try:
                    date, intvs = parse(l)
                    for start, end in intvs:
                        start = int(start * 2)
                        end = int(end * 2)
                        for h in range(start, end):
                            hrs[h] += 1
                except Exception:
                    print("The following is not properly formatted:\n", l)
                total_days += 1

    print(f"\nTotal # days = {total_days}; \n"
          f"Average sleep time = {sum(hrs) / 2 / total_days:.2f} hrs")
    for i in range(48):
        print(f"{i / 2:.1f}   {hrs[i] / total_days * 100:.1f} %")


def avg(yrs=(17, 18, 19, 20, 21, 22), end_date=(22, 5, 22)):
    """
    Output sleep intervals for each month into a file, to be visualized by `vis.js`
    Assume intervals() is already run, and all input is valid
    """
    mo = 8  # start from 2017.8
    days = 0  # days of month
    hrs = [0] * 48  # 48 half-hour intervals
    with open('scripts/sleep/months.csv', 'w') as w1, open('scripts/sleep/months.txt', 'w') as w2:
        w1.write("yr,mo," + ','.join([str(x * 0.5) for x in range(48)]) + '\n')
        w2.write('data = [')
        for yr in yrs:
            file = f"diary/sleep_{yr}.txt"
            with open(file) as f:
                for l in f:
                    if len(l) < 2:
                        continue
                    date, intvs = parse(l)
                    cur_mo = int(date.split('.')[0])
                    cur_day = int(date.split('.')[1])
                    if cur_mo != mo or (yr, cur_mo, cur_day) == end_date:
                        y = yr if mo != 12 else yr - 1
                        print(f'20{y}-{mo} avg sleep: {sum(hrs) / 2 / days:.2f} hrs')
                        if days < 10:
                            print(f'< 10 entries in month {y}-{mo}; month dropped')
                        else:
                            # fixme:
                            w1.write(f"{y},{mo},")
                            w1.write(','.join([str(int(n / days * 1000)) for n in hrs]) + '\n')
                            w2.write(f"[{y},{mo},")
                            w2.write(','.join([str(int(n / days * 1000)) for n in hrs]) + '],\n')
                        mo = cur_mo
                        days = 0
                        hrs = [0] * 48

                    for start, end in intvs:
                        start = int(start * 2)
                        end = int(end * 2)
                        for h in range(start, end):
                            hrs[h] += 1
                    days += 1
        w2.write(']\n')


avg((17, 18, 19, 20, 21, 22), (22, 5, 22))
# intervals([21, 22])
# intervals()




# ----------- obsolete methods --------------


def gen_dates():
    DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for i in range(12):
        for j in range(DAYS[i]):
            print(f"{i+1}.{j+1} - ")


def process_vandy():
    with open('diary/tmp.txt') as f:
        for l in f:
            if l == '\n':
                print()
                continue
            l = l[:-1].split('\t')
            date = l[0].split('-')
            if len(l) != 3 and len(l) != 5:
                raise Exception
            if l[1] and l[1][0] == '-':
                print(f'{24 + float(l[1])} 24')
                l[1] = '0'
            if len(l) == 3:
                print(f'{date[0]}.{date[1]} - {l[1]} {l[2]}')
            elif len(l) == 5:
                print(f'{date[0]}.{date[1]} - {l[1]} {l[2]}, {l[3]} {l[4]}')
