""" 2021-06-16
performs iteration through all txt files for D5 to calculate stats, etc.
"""


import os
from scripts.build_diary import PERIODS

if __name__ == '__main__':
    period_i = 0  # index in the PERIOD array
    period = PERIODS[period_i][0]

    max_n, dn = 0, 0

    for i in range(1, PERIODS[-1][1] + 1):  # go thru each Diary entry in reverse order
        # get the date of the Diary
        in_file = f'../d5/{period}/{i}.txt'
        if i == PERIODS[period_i][1] and i < PERIODS[-1][1]:  # end of current statistical period
            period_i += 1
            period = PERIODS[period_i][0]
        if not os.path.exists(in_file):  # if source D5 txt file does not exist, skip it
            continue
        with open(in_file) as fr:
            for l in fr:
                if '983' in l and '合作' in l:
                    print(i, l)

    print(max_n, dn)
