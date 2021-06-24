"""
In friends.csv, use `#` to comment out people to not yet include in the HTML document
"""

from scripts.templates import *  # base directory is jazonjiao.github.io/


def generate_friends_html_body(lines):
    colors = ['black', 'black', 'black', 'black']

    tbody = ''
    for l in lines:
        if len(l) < 2:
            continue
        if l.count(',') != 4 or l[0] == '#':  # assumes that there are 4 commas (5 columns)
            continue
        num, nat, gen, bs, msphd = tuple(l[:-1].split(','))
        gc = 'b_' if gen == '♂' else 'g_'
        tbody += f"""<tr>
      <th scope="row">{num}</th><td>{nat}</td><td class="{gc}">{gen}</td><td>{bs}</td><td>{msphd}</td>
    </tr>"""

    return f"""
<div class="container my-4 px-2 col-12 col-sm-12 col-md-10 col-lg-9 mx-auto">
  <table class="table table-sm">
    <thead><tr>
      <th scope="col">#</th>
      <th scope="col">国籍</th>
      <th scope="col">性别</th>
      <th scope="col">本科</th>
      <th scope="col">研究生</th>
    </tr></thead>
    <tbody>
    {tbody}
    </tbody>
  </table>
"""


if __name__ == "__main__":
    in_file = '../diary/friends.csv'
    out_file = '../diary/friends.html'

    with open(in_file) as fr, open(out_file, 'w') as fw:
        fw.write(head(f'Jazon Jiao · Friends', n_layers=1, lang='zh') + nav(n_layers=1))

        # skip header
        next(fr)
        fw.write(generate_friends_html_body(fr.readlines()))

        fw.write(f'{footer("EMPTY")}\n</div>\n</body>\n')



