# HTML templates


def head(title, n_layers=1, lang='en'):
    root_dir = '../' * n_layers
    if lang == 'en':
        font = f'<link href="{root_dir}style/en-font.css" rel="stylesheet">'
    elif lang == 'zh':
        font = f'<link href="{root_dir}style/cn-font.css" rel="stylesheet">'
    else:
        raise Exception('Language error')
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
  {font}
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


# note: remember to close the divs
def container(px=3):
    return f'\n<div class="container my-4 px-{px} col-12 col-sm-12 col-md-10 col-lg-9 mx-auto">\n'


def footer(path):
    return f"""
<footer class="pt-3 mt-4 text-muted border-top">
&copy; 2021 Jazon Jiao<br/>
</footer>
"""
