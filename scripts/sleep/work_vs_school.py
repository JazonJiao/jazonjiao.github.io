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


def in_range(date):
    mo, day = int(date.split(".")[0]), int(date.split('.')[1])
    return mo < 7 or (mo == 7 and day <= 18)


def intervals():
    """
    Prints the percentage of time I'm asleep for each half-hour interval of the day,
    for selected years
    """
    total_days = 0
    hrs = [0] * 48  # 48 half-hour intervals
    file = f"diary/sleep_22.txt"
    with open(file) as f:
        for l in f:
            if len(l) < 2:
                continue
            try:
                date, intvs = parse(l)
                if in_range(date):
                    continue
                for start, end in intvs:
                    start = int(start * 2)
                    end = int(end * 2)
                    for h in range(start, end):
                        hrs[h] += 1
            except Exception:
                print("The following is not properly formatted:\n", l)
            total_days += 1

    print(f"Daytime (11-23) sleep:")
    print(f"Average hours per day: {sum(hrs[22:46]) / 2 / total_days:.2f} hours")
    print(f"Percentage: {sum(hrs[22:46]) / sum(hrs) * 100:.2f}%")


intervals()
