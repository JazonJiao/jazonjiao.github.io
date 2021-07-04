""" 2021-06-12
Run this file locally to build HTML files for D5 pages and the archive page

Note that some difference exists between my own version of Diary and the online version,
mostly for category-4 texts.


=== Format description of input Diary txt files: ===

The majority of my Diary consists of plain text. Other features include:

- Title <h1>
The first line should be the title of the Diary, of the form `D5Pxxx-yymmdd`.

- Subtitle <h2>
If there is a subtitle, then that line is surrounded by <h2> tags, such as
`<h2>Trip to Northern Capital</h2>`

- Sections <h3>
Some diary such as D5P84 is organized into sections. Each section header starts with the [h3]
identifier.

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
converted to hyperlinks to that Diary. todo: add support for D4F (e.g. D5P230-190726)


=== Abbreviations used in my Diary that is to be replaced in the online version ===
GR2, GR3, GR4


=== Output HTML file format ===

h1 tag: Diary titles
h2 tag: Diary subtitles
h3 tag: Diary section headers
h4 tag: Statistical Period titles in d5/index.html, like "2019 Spring"

- id (used for anchoring)
(1) Diary title has id = "0".
(2) Each paragraph has id = the paragraph's index (1-indexed), such as "7", "15", etc.
(3) Each section header (h3) has id = "part#", such as "part1", "part6", etc.

"""
import os, re
from scripts.templates import *  # base directory is jazonjiao.github.io/

# My Diaries are divided into statistical periods by time.
# Each year has 3 stat periods, denoted `a`, `b`, `c`.
# The following lists the ENDING D5 No. for each period (inclusive).
# The D5 No. for the last period is the No. for the latest (i.e. current) Diary.
# The array also hardcodes the word count for that period, as well as
# percentages for 4 categories.
PERIODS = [
    ('17a', 45, '17 Spring', 'null', 'null', 'null', 'null', 'null'),  # 45 entries
    ('17b', 71, '17 Summer', 'null', 'null', 'null', 'null', 'null'),  # 26 entries
    ('17c', 105, '17 Autumn', 36685, 20.7, 26.9, 19.1, 33.3),  # 34 entries
    ('18a', 138, '18 Spring', 26730, 31.3, 21.2, 18.3, 29.2),  # 33 entries
    ('18b', 155, '18 Summer', 12302, 36.9, 16.1, 33.7, 13.4),  # 23 entries
    ('18c', 183, '18 Autumn', 18986, 41.7, 17.9, 29.0, 11.5),  # 28 entries
    ('19a', 209, '19 Spring', 19179, 43.1, 19.5, 26.7, 10.7),  # 26 entries
    ('19b', 233, '19 Summer', 20293, 39.9, 31.4, 25.2, 3.4),  # 24 entries
    ('19c', 276, '19 Autumn', 33733, 18.4, 31.3, 7.4, 43.0),  # 43 entries
    ('20a', 311, '2020 春', 56021, 14.3, 68.5, 9.6, 7.7),  # 35 entries
    ('20b', 339, '2020 夏', 44368, 23.7, 37.2, 22.0, 17.1),  # 28 entries
    ('20c', 364, '2020 秋', 'null', 'null', 'null', 'null', 'null'),  # 25 entries
    ('21a', 389, '2021 春', 'null', 'null', 'null', 'null', 'null'),  # 25 entries
    ('21b', 395, '2021 夏', 'null', 'null', 'null', 'null', 'null')
]


# ---------------------------------------------------------------
# ------------ methods that return html templates ---------------


def stats_table():
    # colors for the 4 categories
    colors = ['#e96700',
              'green',
              'dodgerblue',
              'rebeccapurple']
    txtcs = ['#c94900', '#096909', '#0969b9', '#563d7c']
    bgcolor = '#ffe7c9'
    tbody = ''
    for period_id, _, period_name, wc, c1, c2, c3, c4 in reversed(PERIODS[2:]):  # ignore 17a, 17b for now
        wc_unit = 'words' if period_id < '20a' else '字'
        tbody += f"""
    <tr>
      <th scope="row"><a href="#{period_id}">{period_name}</a></th>
      <td>{wc} {wc_unit}</td>
      <td style="color: {colors[0]}">{c1} %</td>
      <td style="color: {colors[1]}">{c2} %</td>
      <td style="color: {colors[2]}">{c3} %</td>
      <td style="color: {colors[3]}">{c4} %</td>
    </tr>"""

    return f"""
<div class="container my-4 px-2 col-12 col-sm-12 col-md-10 col-lg-9 mx-auto">
  <table class="table table-sm">
    <thead>
    <tr>
      <th scope="col" style="color: darkred;">Period</th>
      <th scope="col">Word Count</th>
      <th scope="col" style="color: {colors[0]}">Learning</th>
      <th scope="col" style="color: {colors[1]}">Growth</th>
      <th scope="col" style="color: {colors[2]}">Life</th>
      <th scope="col" style="color: {colors[3]}">Love</th>
    </tr>
    </thead>
    <tbody>
{tbody}
    </tbody>
  </table>
</div>

{container(additional_class_name=" fs_sm")}
<h1 style="text-align: center; margin-top: 97px; margin-bottom: 37px;">【 Categories 】</h1>
My diary content falls into one of 4 categories. What each category means shifts greatly over time, 
but the principle of division into
<span style="color: {colors[0]}">Learning</span>,
<span style="color: {colors[1]}">Growth</span>,
<span style="color: {colors[2]}">Life</span>, and
<span style="color: {colors[3]}">Love</span> remains the same.
</div>

<!-- description of 4 categories -->
<div class="container px-xs-5 px-sm-3 px-md-0 py-4">
  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4">
    <div class="col">
      <div class="card h-100" style="border-color: {colors[0]}; background: {bgcolor}; box-shadow: 3px 3px 9px -4px #999;">
        <div class="card-body">
          <h5 class="card-header fw-bold" style="color: {colors[0]}; border-bottom-color: {colors[0]};">1. Learning (学习)</h5>
          <p class="mt-3 categ">
<ul class="cat" style="color: {txtcs[0]};">
<li class="cat">Technical aspects of my work, projects, or research; study notes</li>
<li class="cat">Study methods and resources; time management</li>
<li class="cat">Evaluation of my study/work efficiency; reflection on my attitudes</li>
<li class="cat">Academic interests</li>
<li class="cat">Course logistics</li>
<li class="cat">Study plans and goals; self-encouragements</li>
</ul>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card h-100" style="border-color: {colors[1]}; background: {bgcolor}; box-shadow: 3px 3px 9px -4px #999;">
        <div class="card-body">
          <h5 class="card-header fw-bold" style="color: {colors[1]}; border-bottom-color: {colors[1]};">2. Growth (成长)</h5>
          <p class="mt-3 categ">
<ul class="cat" style="color: {txtcs[1]};">
<li class="cat">Behavioral and political aspects of work; leadership skills</li>
<li class="cat">Career planning</li>
<li class="cat">Application to programs (e.g. grad school, internships)</li>
<li class="cat">Personal values; life philosophy</li>
<li class="cat">life trajectories of myself and others; personality analysis</li>
<li class="cat">Interpersonal relationships</li>
</ul>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card h-100" style="border-color: {colors[2]}; background: {bgcolor}; box-shadow: 3px 3px 9px -4px #999;">
        <div class="card-body">
          <h5 class="card-header fw-bold" style="color: {colors[2]}; border-bottom-color: {colors[2]};">3. Life (生活)</h5>
          <p class="mt-3 categ">
<ul class="cat" style="color: {txtcs[2]};">
<li class="cat">Fun activity with friends; my hobbies</li>
<li class="cat">Travel logs; world cultures</li>
<li class="cat">Current events; societal issues</li>
<li class="cat">physical and mental health; sleep conditions</li>
<li class="cat">Food, housing, climate, pets, money...</li>
</ul>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card h-100" style="border-color: {colors[3]}; background: {bgcolor}; box-shadow: 3px 3px 9px -4px #999;">
        <div class="card-body">
          <h5 class="card-header fw-bold" style="color: {colors[3]}; border-bottom-color: {colors[3]};">4. Love (情感)</h5>
          <p class="mt-3 categ">
<ul class="cat" style="color: {txtcs[3]};">
<li class="cat">My feelings for, and interactions with, the girls who I like(d) and/or who liked me</li>
<li class="cat">Analysis of my past love experiences</li>
<li class="cat">Viewpoint on romantic relationships</li>
</ul>
        </div>
      </div>
    </div>
  </div>
  <div class="my-4 border-top"></div>
</div>
<h1 style="text-align: center; margin-bottom: 17px;">【 Entries 】</h1>
"""


def archive_notes():
    return f"""
<h1 style="text-align: center; margin-top: 67px; margin-bottom: 37px;">【 Notes 】</h1>
<ul>
<li class="cat">Friend list is <a href="./friends/">here</a>.</li>
<li class="cat">Not all Diaries are published; I’m usually less selective on older entries.
The statistics above are for the full version of my Diary.</li>
<li class="cat">Sometimes, the category of a piece of Diary text is ambiguous, so the
stats aren’t 100% accurate. That’s fine, since most tallies need to deal with fuzzy definitions
(for example, figuring out the religious decomposition of a country’s population).</li>
</ul>
"""


def toplinks(i):
    s = '<p><a href="../../">Archive</a> '
    if i > 1:
        s += f'<a href="../{i - 1:03d}">← Prev</a> '
    if i < PERIODS[-1][1]:
        s += f'<a href="../{i + 1:03d}">Next →</a>'
    s += '</p>\n'
    return s


circled_n = '⓪ ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ ㉑ ㉒ ㉓ ㉔ ㉕ ' \
            '㉖ ㉗ ㉘ ㉙ ㉚ ㉛ ㉜ ㉝ ㉞ ㉟ ㊱ ㊲ ㊳ ㊴ ㊵ ㊶ ㊷ ㊸ ㊹ ㊺ ㊻ ㊼ ㊽ ㊾ ㊿'


# ----------------------------------------------------------
# ------------ methods that build html files ---------------

def generate_archive_html():
    def write_period_name(fw, p):
        _ = ord(p[2]) - ord('a')
        if p[:2] >= '20':
            name = ['年 1 ~ 4 月', '年 5 ~ 8 月', '年 9 ~ 12 月'][_]
        else:
            name = ['Jan. — Apr.', 'May — Aug.', 'Sept. — Dec.'][_]
        fw.write(f'<h4 id="{p}">20{p[:2]} {name}</h4>\n' +
                 f'<div class="row d-flex" style="margin-bottom: 29px;">\n')

    # === end of helper function definitions ===

    out_file = '../d5/index.html'
    period_i = len(PERIODS) - 1  # index in the PERIOD array
    period = PERIODS[period_i][0]

    with open(out_file, 'w') as fw:
        # write head and nav
        fw.write(head('Jazon Jiao · D5 archive', n_layers=1, lang='zh') + nav(n_layers=1))
        # write title
        fw.write('\n<h1 style="text-align: center; margin-bottom: 67px;">【 Diary 5 Archive 】</h1>')
        # write the table for Diary statistics
        fw.write(stats_table())
        # write bootstrap container and <p> tag
        fw.write(container(2))
        # first statistical period
        write_period_name(fw, period)

        for i in range(PERIODS[-1][1], 0, -1):  # go thru each Diary entry in reverse order
            if i == PERIODS[period_i - 1][1]:  # end of current statistical period
                fw.write('</div>\n')
                period_i -= 1
                period = PERIODS[period_i][0]
                write_period_name(fw, period)

            # get the date of the Diary
            in_file = f'../d5/{period}/{i}.txt'
            if not os.path.exists(in_file):  # if source D5 txt file does not exist, skip it
                continue
            with open(in_file) as fr:
                d5p = fr.readline()[3:-1]

            # NOTE: THE href PATH IS RELATIVE TO d5/archive HERE!!!
            fw.write(f'<div class="col-4"><a href="p/{i:03d}/">D5p{d5p}</a></div>\n')

        # close tags
        fw.write(f'</div>{archive_notes()}{footer("EMPTY")}\n</div>\n</div>\n</body>\n')


def generate_d5_html(start_i=1, end_i=PERIODS[-1][1]):
    """
    builds Diary folders and index.html files

    :param start_i: starting Diary No. to build (inclusive)
    :param end_i: ending Diary No. to build (inclusive)
    """

    def insert_spaces(line):
        """ 2021-06-30
        Insert spaces between Chinese characters and alphanumeric chars (letters, numbers)
        """
        def is_cn_punc(char):
            return char in '，。？！、：；（）《》【】…'

        en_words = re.split(u"[^A-Za-z0-9_,.:+%()<>’°/@&\[\]-]+", line)
        zh_words = re.split(u"[A-Za-z0-9_,.:+%()<>’°/@&\[\]-]+", line)
        if zh_words[0] == '':
            zh_words = zh_words[1:]
        res = ''
        for i in range(len(en_words)):
            if i > 0 and not is_cn_punc(zh_words[i - 1][-1]):
                res += ' '
            res += en_words[i]
            if i >= len(zh_words):
                break
            if not is_cn_punc(zh_words[i][0]):
                res += ' '
            res += zh_words[i]

        return res

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
        in_file = f'../d5/{period}/{i}.txt'
        out_path = f'../d5/p/{i:03d}'  # `03d` makes `1` -> `001`, `19` -> `019`, etc.
        if i == PERIODS[period_i][1] and i < PERIODS[-1][1]:  # end of current statistical period
            period_i += 1
            period = PERIODS[period_i][0]
        if not os.path.exists(in_file):  # if source D5 txt file does not exist, skip it
            continue

        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        with open(in_file) as fr, open(out_path + '/index.html', 'w') as fw:
            # write head and nav-bar
            lang = 'en' if i < 277 else 'zh'
            fw.write(head(f'Jazon Jiao · D5p{i}', n_layers=3, lang=lang) + nav(n_layers=3))

            # write container and header (D5p#)
            fw.write(container())
            d5p = fr.readline()[:-1]
            fw.write(toplinks(i) + f'<h1 id="0">{d5p}</h1>\n<div class="row d-flex" id="rdf">\n')

            # write body
            j = 0  # paragraph count
            h = 0  # h3 section header count
            for l in fr:
                if len(l) > 2:   # categorized paragraph (fixme)
                    if l[2] == '`': l = l[3:]
                    if l[1] == '`': l = l[2:]
                # insert spaces into Chinese diary
                if lang == 'zh':
                    l = insert_spaces(l)
                if len(l) >= 4 and l[0] == '<':   # start/end quotes; h2 subtitles
                    fw.write(f'{l}')
                    continue
                if len(l) > 4 and l[:4] == '[h3]':  # h3 section headers
                    h += 1
                    fw.write(f'<h3 id="part{h}">{l[4:-1]}</h3>\n')
                    continue
                # create links
                l = insert_diary_links(l)
                j += 1
                fw.write(f'<p id="{j}"><span>{circled_n[j * 2]}</span> {l[:-1]}</p>\n')

            # close the tags
            fw.write(f'</div>{footer(out_path)}</div>\n</body>\n')
            print(i, period)
            # end of the i-th Diary document


if __name__ == '__main__':
    generate_archive_html()
    generate_d5_html(72, 389)  # fixme



