""" 2021-06-12
Run this file locally to build HTML files for D5 pages and the archive page

Note that some difference exists between my own version of Diary and the online version,
mostly for category-4 texts.


=== Format description of input Diary txt files: ===

The majority of my Diary consists of plain text. Other features include:

- Title
The first line should be the title of the Diary, of the form `D5Pxxx-yymmdd`.

- Category
"Categorized paragraphs" are paragraphs preceded by 3 characters representing its category,
such as "12`".

- Quotes
Some parts of my Diary quotes (1) my non-Diary writings, such as letters to others;
(2) my past Diary; or (3) others' verbatim words.
These quotes should be surrounded by `<em>` at the beginning and `</em>` at the end.
These indicators be separate lines and will be copied into the HTML document.

- Intra-site links
I sometimes refer to my previous or future Diary in the form of `D5Pxxx`. These will be
converted to hyperlinks to that Diary.


=== Abbreviations used in my Diary that is to be replaced in the online version ===
GR2, GR3, GR4
"""
import os, re

# My Diaries are divided into statistical periods by time.
# Each year has 3 stat periods, denoted `a`, `b`, `c`.
# The following lists the ending D5 No. for each period (inclusive).
# The No. for the last period is the No. for the latest (i.e. current) Diary.
PERIODS = [('17a', 45), ('17b', 71), ('17c', 105),
           ('18a', 138), ('18b', 154), ('18c', 183),
           ('19a', 209), ('19b', 232), ('19c', 276),
           ('20a', 311), ('20b', 339), ('20c', 364),
           ('21a', 389), ('21b', 395)]


# ---------------------------------------------------------------
# ------------ methods that return html templates ---------------


def head(title, n_layers=1):
    root_dir = '../' * n_layers
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- for mobile devices -->
  <title>{title}</title>

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css"
        integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x"
        crossorigin="anonymous" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4"
          crossorigin="anonymous"></script>
  <script
      src="https://code.jquery.com/jquery-3.6.0.min.js"
      integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
      crossorigin="anonymous"></script>

  <link href="{root_dir}style/index.css" rel="stylesheet">
  <link href="{root_dir}style/diary.css" rel="stylesheet">

  <link rel="icon" href="{root_dir}file/icon/brainy.ico" type="image/x-icon"/>
</head>

<body class="warm-theme">
"""


def nav(n_layers=2):
    root_dir = '../' * n_layers
    return f"""
<!-- Navigation -->
<nav class="warm-theme navbar sticky-top navbar-expand-sm navbar-light" aria-label="Third navbar example">
  <div class="container-fluid mt-1 mx-2">
    <a href="{root_dir}">
      <img src="{root_dir}file/icon/jazon-logo.png" alt="logo" id="jazon-logo"/>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample03"
            aria-controls="navbarsExample03" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarsExample03">
      <ul class="navbar-nav ms-auto fs-5">
        <li class="nav-item"> <a class="nav-link" href="{root_dir}about">About</a> </li>
        <li class="nav-item"> <a class="nav-link" href="{root_dir}blog">Blog</a> </li>
        <li class="nav-item"> <a class="nav-link" href="{root_dir}proj">Projects</a> </li>
        <li class="nav-item"> <a class="nav-link" href="{root_dir}diary">Diary</a> </li>
      </ul>
    </div>
  </div>
</nav>
"""


def toplinks(i):
    s = '<a href="../../">Archive</a>\n'
    if i > 1:
        s += f'<a href="../{i - 1:03d}">← Prev</a>\n'
    if i < PERIODS[-1][1]:
        s += f'<a href="../{i + 1:03d}">Next →</a>\n'
    return s


# note: remember to close the divs
def container(px=3):
    return f'\n<div class="container my-4 px-{px} col-12 col-sm-12 col-md-10 col-lg-9 mx-auto">\n'


# ----------------------------------------------------------
# ------------ methods that build html files ---------------

def generate_archive_html():
    def write_period_name(fw, p):
        _ = ord(p[2]) - ord('a')
        if p[:2] >= '20':
            name = ['年 1 ~ 4 月', '年 5 ~ 8 月', '年 9 ~ 12 月'][_]
        else:
            name = ['Jan. — Apr.', 'May — Aug.', 'Sept. — Dec.'][_]
        fw.write(f'<h4>20{p[:2]} {name}</h4>\n' +
                 f'<div class="row d-flex" id="{p}" style="margin-bottom: 29px;">\n')

    # === end of helper function definitions ===

    out_file = 'd5/index.html'
    period_i = len(PERIODS) - 1  # index in the PERIOD array
    period = PERIODS[period_i][0]

    with open(out_file, 'w') as fw:
        # write head and nav
        fw.write(head('Jazon Jiao · D5 archive', n_layers=1) + nav(n_layers=1))
        # write bootstrap container and <p> tag
        fw.write(container(2) + '\n')
        # first statistical period
        write_period_name(fw, period)

        for i in range(PERIODS[-1][1], 0, -1):  # go thru each Diary entry in reverse order
            if i == PERIODS[period_i - 1][1]:  # end of current statistical period
                fw.write('</div>\n')
                period_i -= 1
                period = PERIODS[period_i][0]
                write_period_name(fw, period)

            # get the date of the Diary
            in_file = f'd5/{period}/{i}.txt'
            if not os.path.exists(in_file):  # if source D5 txt file does not exist, skip it
                continue
            with open(in_file) as fr:
                d5p = fr.readline()[3:-1]

            # NOTE: THE href PATH IS RELATIVE TO d5/archive HERE!!!
            fw.write(f'<div class="col-4"><a href="p/{i:03d}/">D5p{d5p}</a></div>\n')

        # close tags
        fw.write('</div>\n<br/><br/><br/><br/>\n</div>\n</div>\n</body>\n')


def generate_d5_html(start_i=1, end_i=PERIODS[-1][1]):
    """
    builds Diary folders and index.html files

    :param start_i: starting Diary No. to build (inclusive)
    :param end_i: ending Diary No. to build (inclusive)
    """

    def insert_spaces(line):
        """
        Insert spaces between Chinese characters and alphanumeric chars (letters, numbers)
        Adapted from https://blog.csdn.net/qq_26064989/article/details/107517919
        """
        str1 = re.sub(r"([A-Za-z]+)([\u4e00-\u9fa5]+)", r'\1 \2', line)
        str2 = re.sub(r"([\u4e00-\u9fa5]+)([A-Za-z]+)", r"\1 \2", str1)
        str3 = re.split(r"([\u4e00-\u9fa5])", str2)

        wordlist = [ss + " " for ss in str3]
        return "".join(wordlist)

    def insert_diary_links(line):
        """
        `line` should be one single paragraph, since this code breaks if
        (1) two formats, e.g. `D5P84` and `D5P84-171008`, appear simultaneously in the input
        (2) one Diary entry appears > 1 times in the input
        """
        # r2 = r"D5(P|p)(\d+)-\d{6}"
        list = re.findall(r"D5P(\d+)", line)  # find all D5 numbers that appeared
        for d5_number in list:
            idx = line.find(f'D5P{d5_number}')  # d5_number is str here
            m = len(f'D5P{d5_number}')
            href = f'<a href="../{int(d5_number):03d}/">'
            if line[idx + m] == '-':  # of the form D5P#-yymmdd
                line = f'{line[:idx]}{href}{line[idx: idx + m + 7]}</a>{line[idx + m + 7:]}'
            else:  # of the form D5P#
                line = f'{line[:idx]}{href}{line[idx: idx + m]}</a>{line[idx + m:]}'
        return line

    # === end of helper function definitions ===

    # initialize the current period
    period_i = 0
    for _ in range(len(PERIODS) - 1, -1, -1):
        if start_i > PERIODS[_][1]:
            break
        period_i = _
    period = PERIODS[period_i][0]

    # go thru each Diary No.
    for i in range(start_i, end_i + 1):
        in_file = f'd5/{period}/{i}.txt'
        if not os.path.exists(in_file):  # if source D5 txt file does not exist, skip it
            continue

        out_path = f'd5/p/{i:03d}'      # `03d` makes `1` -> `001`, `19` -> `019`, etc.
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        with open(in_file) as fr, open(out_path + '/index.html', 'w') as fw:
            # write head and nav-bar
            fw.write(head(f'Jazon Jiao · D5p{i}', n_layers=3) + nav(n_layers=3))

            # write container and header (D5p#)
            fw.write(container())
            d5p = fr.readline()[:-1]
            fw.write(toplinks(i) +
                     f'<h1>{d5p}</h1>\n<div class="row d-flex" id="rdf" style="margin-bottom: 199px;">\n')

            # write body
            j = 0  # paragraph count
            for l in fr:
                if len(l) > 2 and l[2] == '`':   # categorized paragraph (fixme)
                    l = l[3:]
                if len(l) > 4 and l[0] == '<':   # start/end quotes
                    fw.write(f'{l}')
                    continue  # i.e., else:
                # create links
                l = insert_diary_links(l)
                j += 1
                fw.write(f'<p id="p{j + 1}">{l[:-1]}</p>\n')

            # close the tags
            fw.write('</div>\n</div>\n</body>\n')
            # end of the i-th Diary document

        if i == PERIODS[period_i][1]:     # end of current statistical period
            period_i += 1
            period = PERIODS[period_i][0]


if __name__ == '__main__':
    generate_archive_html()
    generate_d5_html(155, 219)  # fixme


