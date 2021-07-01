# encoding=utf-8

"""
Expected format of Diary.txt:

Each statistical period begins by "|" plus the name of the period, e.g. "|2017 Fall"
Each line is either the title, e.g. "D5P77-170828", or body text of Diary
Body text start with a 2-digit number indicating type, followed by a "`" character

Starting from Chinese Diary, only 1 digit is used to denote type
"""

import re

DIARY_FILE = 'Diary.txt'  # 'Diary_cn.txt'

periods = ['2017 Fall', '2018 Spring', '2018 Summer', '2018 Fall', '2019 Spring', '2019 Summer',
           '2019 Fall', '2020 Spring']


def count_en_words(line):
    return len(line.split()) + line.count('—')


def tally_type():
    OUT_FILE = 'tally_type.csv'

    d = {}
    types = ['11', '12', '13', '14', '21', '22', '23', '24', '25',
             '31', '32', '33', '34', '41', '42', '43', '44']  # 44 is not yet assigned

    with open(DIARY_FILE, encoding='utf-8') as f:
        cur_period = ''
        for line in f:
            if not line:  # empty line
                continue
            if line[0] == '|':  # start of new statistical period
                cur_period = line[1: -1]
                d[cur_period] = {s: 0 for s in types}
            elif '`' not in line:
                continue
            else:
                type = line[:2]
                if type not in types:
                    print('ERROR')
                if cur_period != '2020 Spring':  # English word count fixme
                    d[cur_period][type] += count_en_words(line)
                else:
                    pass

    with open(OUT_FILE, 'wb') as f:
        f.write(bytes('Period,' + ','.join(types) + '\n', 'utf8'))
        for cur_period in periods:
            print(cur_period)
            dic = d[cur_period]
            f.write(bytes(cur_period + ',', 'utf8'))

            print('Total: ' + str(sum([v for v in dic.values()])))
            print('SUM 1: ' + str(dic['11'] + dic['12'] + dic['13'] + dic['14']))
            print('SUM 2: ' + str(dic['21'] + dic['22'] + dic['23'] + dic['24']))
            print('SUM 3: ' + str(dic['31'] + dic['32'] + dic['33'] + dic['34']))
            print('SUM 4: ' + str(dic['41'] + dic['42'] + dic['43'] + dic['44']))
            for k, v in sorted(dic.items()):
                print(k + ': ' + str(v)),
                f.write(bytes(str(v) + ',', 'utf8'))

            print('\n')
            f.write(bytes('\n', 'utf8'))


def tally_people():
    OUT_FILE = 'tally_people.csv'

    vandy_core = ['493', '495', '293', '983', '329', '671', '979', '982', '120',
                  '139', '133', '026', '359']

    vandy_friends = ['355', '462', '468', '474', '477', '478', '481', '482', '488', '489',
                     '491', '494', '496', '498', '876', '545', '565', '698']

    nfls_friends = ['457', '621', '717']

    other_friends = ['458', '287', '042', '962']

    special = ['697']

    people = vandy_core + vandy_friends + nfls_friends + other_friends

    d = {}
    for p in people:
        d[p] = {}
        with open(DIARY_FILE) as f:
            cur_period = ''
            for line in f:
                if not line:  # empty line
                    continue
                if line[0] == '|':  # start of new statistical period
                    cur_period = line[1: -1]
                    d[p][cur_period] = 0
                else:
                    cnt = 0
                    if line[:3] == p:
                        cnt += 1
                    for i in range(1, len(line) - 4):
                        # fixme: \b matches word boundaries
                        if line[i: i + 3] == p and \
                                not line[i - 1].isdigit() and not line[i + 4].isdigit():
                            cnt += 1
                    d[p][cur_period] += cnt
        print("Finished: " + p)

    totals = {p: 0 for p in people}
    for person, dic in d.items():
        totals[person] = sum([v for v in dic.values()])

    sorted_people = [p for p, v in sorted(totals.items(), key=lambda x: -x[1])]

    with open(OUT_FILE, 'wb') as f:
        f.write('Person,' + ','.join(periods) + '\n')
        for p in sorted_people:
            f.write(p + ',')
            for t in periods:
                f.write(str(d[p][t]) + ',')

            f.write('\n')


def count_cn_words(line):  # count words in a line of Chinese Diary text
    wc = 0
    line = line[:-1]
    alnum_words = re.split(u"[^A-Za-z0-9_\-]+", line)  # alphanumeric words
    wc += len(alnum_words)  # count number of words
    if wc > 0 and alnum_words[0] == '':
        wc -= 1
    if wc > 0 and alnum_words[-1] == '':
        wc -= 1
    cn_words = re.split(u"[A-Za-z0-9_.\- ]+", line)  # include spaces
    wc += sum(len(s) for s in cn_words)  # count chinese characters
    return wc


def tally_type_cn():
    d = {}

    with open(DIARY_FILE, encoding='utf-8') as f:
        cur_period = ''
        for line in f:
            if not line:  # empty line
                continue
            if line[0] == '|':  # start of new statistical period
                cur_period = line[1: -1]
                d[cur_period] = [0, 0, 0, 0]
            elif '`' not in line:
                continue
            else:
                type = int(line[0])
                if type < 1 or type > 4:
                    raise Exception('ERROR: unsupported type')
                type -= 1  # convert to array index
                # d[cur_period][type] += len(line[2:-1])
                d[cur_period][type] += count_cn_words(line[2:-1])

    for cur_period in periods:
        print(cur_period)
        arr = d[cur_period]

        tot = sum(arr)
        print(f'Total: {tot}')
        print(f'SUM 1: {arr[0]}, {arr[0] / tot * 100:.1f}%  = {arr[0] * 3 / 5:.1f} words')
        print(f'SUM 2: {arr[1]}, {arr[1] / tot * 100:.1f}%  = {arr[1] * 3 / 5:.1f} words')
        print(f'SUM 3: {arr[2]}, {arr[2] / tot * 100:.1f}%  = {arr[2] * 3 / 5:.1f} words')
        print(f'SUM 4: {arr[3]}, {arr[3] / tot * 100:.1f}%  = {arr[3] * 3 / 5:.1f} words')


def test():
    wc = 0
    with open('test_for_Chinese_word_cnt.txt', encoding='utf-8') as f:
        for line in f:
            line = line[:-1]
            alnum_words = re.split(u"[^A-Za-z0-9_.-]+", line)  # alphanumeric words
            wc += len(alnum_words)  # count number of words
            if wc > 0 and alnum_words[0] == '':
                wc -= 1
            if wc > 0 and alnum_words[-1] == '':
                wc -= 1
            print(alnum_words)
            cn_words = re.split(u"[A-Za-z0-9_. -]+", line)  # include spaces
            print(cn_words)
            wc += sum(len(s) for s in cn_words)  # count chinese characters
    return wc


if __name__ == '__main__':
    print(test())
    tally_type_cn()
