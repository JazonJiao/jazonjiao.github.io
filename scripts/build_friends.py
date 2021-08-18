"""
In friends.csv, if
    (1) there is a `#` at the beginning,
    (2) there are not enough commas
The person is not included in the HTML document

"""

from scripts.templates import *  # base directory is jazonjiao.github.io/


def friends_intro():
    return f"""
<h1 style="text-align: center; margin-bottom: 79px;">
【 <a href="../">D5</a> Friend List 】</h1>
{container(additional_class_name=" fs_sm")}

我在日记中，时常以 3 位数字称呼我的同学朋友们。命名规则：</br>

<ul>
<li>901 ~ 960：代表我的初中同班同学；我初中在 9 班（南外初中共 12 个班），9xx 的后两位数字为学号。</li>
<li>1xx，2xx，...，8xx，01 ≤ xx ≤ 57：默认情况下，此为我同学的高中学号后三位。我高中毕业于南外 2017 届，共 8 个班，每班约 57 人。</li>
<li>下列高中同学也是我 Vandy 本科同学：120、133、139、309、355、413、544、545、619。其中 139 也是我的研究生学弟。</li>
<li>高中之后认识的朋友，最直接的方式是采用姓名首字母的<a href="https://en.wikipedia.org/wiki/Telephone_keypad">九键</a>，比如
“HSN” 对应 476。但由于 WXYZ 都映射至数字 9，中国人名里这些字母的频率又特别高，因此为避免 Hash collision，我也使用其他方法（如名字谐音），很多时候比较随性。</li>
<li>如与高中同学学号有冲突（如 746），则表明我不认识那位高中同学，或者对方为我初中同学，其学号可用 9xx 表示。</li>
<li>前缀为 7 的，是我在 Stanford 认识的同学（“7” 代表 “S”tanford）。</li>
<li>前缀为 4 的，是我在 Vandy 认识的学长学姐；这里是按入学年份算的（我 2017 年本科入学，2020 届毕业）。</li>
<li>前缀为 2 的，代表学弟学妹。</li>
</ul>
列表如下；本科记录毕业届数，研究生记录入学年份。
<br/><br/><br/>
</div>
"""


def generate_friend_table(lines):
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
    out_file = '../d5/friends/index.html'

    with open(in_file) as fr, open(out_file, 'w') as fw:
        fw.write(head(f'Jazon Jiao · Friends', n_layers=2, lang='zh') + nav(n_layers=2))
        fw.write(friends_intro())

        # skip header
        next(fr)
        fw.write(generate_friend_table(fr.readlines()))

        fw.write(f'{footer("EMPTY")}\n</div>\n</body>\n')



