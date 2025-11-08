from pybtex.database.input import bibtex
from pybtex.database import parse_file
import json

color = {
    'title': '#2667ff',
    'authors': '#415a77'
    #safety: 003161
    #efficient: 27391C
}


def get_personal_data():
    name = ["Dongjae", "Jeon"]
    email = "dongjae0324@yonsei.ac.kr"
    scholar = 'https://scholar.google.com/citations?user=SaaN_bAAAAAJ&hl=en'
    # twitter = "Mi_Niemeyer"
    github = "https://github.com/Dongjae0324"
    linkedin = "https://www.linkedin.com/in/dongjae-jeon-a74526255"
    bio_text = f"""
                <p>
    I am a first-year master's student in Computer Science at  
    <a href="https://www.yonsei.ac.kr/en_sc/" target="_blank">Yonsei University</a>,  
    working in the  
    <a href="https://albert-no.github.io/" target="_blank">Artificial Intelligence and Information Systems Lab</a>  
    with Professor <a href="https://albert-no.github.io/" target="_blank">Albert No</a>.<br><br>

    I am specifically interested in generative models,
    where 
    
    My research focuses on <span style="color:#0046FF;">safe and reliable AI</span>, with an emphasis on generative models.  
    Currently, I am interested in advancing Diffusion Language Models (sampling methodologies and architectures).  
    I also pursue the development of <span style="color:#03A791;">efficient AI</span> systems.

    Previously, I have conducted research on <em>Continual Learning</em> in the context of computer vision.  
    My primary goal is to deepen our understanding of how machines perceive and to create methods that enhance their reliability.

    </p>
    <p>Here is my <a href="https://dongjae0324.github.io/assets/pdf/CV_dongjae_jeon.pdf" target="_blank">CV</a>. Feel free to contact me via email if you are interested.</p>

                <p>
                   <a href="https://dongjae0324.github.io/assets/other/bio.txt" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-graduation-cap"></i> Bio</a>
                    <a href="{email}" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="{scholar}" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a href="{github}" target="_blank" style="margin-right: 5px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="{linkedin}" target="_blank" style="margin-right: 5px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <hr>
                <p style="padding-left: 5px;">
                    Template borrowed from 
                    <a href="https://m-niemeyer.github.io/" target="_blank">Here</a>
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Wonje Jeung': 'https://cryinginitial.github.io',
        'Taeheon Kim': 'https://ta3h30nk1m.github.io',
        'Albert No': 'https://albert-no.github.io/team/',
        'Jonghyun Choi': 'https://ppolon.github.io', 
        }

def generate_person_html(persons, coauthor, connection=", ", make_bold=True, make_bold_name='Dongjae Jeon', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        star = "" if string_part_i not in coauthor else "*"
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank" style="color: {color["authors"]}" >{string_part_i}{star}</a>'
        elif string_part_i != make_bold_name:
            string_part_i = f'<span style="color: {color["authors"]}">{string_part_i}{star}</span>'
            
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{string_part_i}{star}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_news_entry(entry):
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    year = entry.get("year", "")
    month = entry.get("month", "")
    content = entry.get("content", "")

    try:
        month_name = month_names[int(month)]
    except:
        month_name = ""

    if month_name and year:
        return f"""<span style="display: inline-block; min-width: 5em;"><b>{month_name} {year}:</b></span> {content}<br>\n"""
    elif year:
        return f"""<span style="display: inline-block; min-width: 6em;"><b>{year}</b></span> {content}<br>\n"""
    else:
        return f"{content}<br>\n"



def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    # ====== Paper Title ======
    s += f"""<a href="{entry.fields['html']}" target="_blank" style="color: {color['title']}">{entry.fields['title']}</a>"""

    # ====== Add Color-Coded Tags ======
    tag_colors = {
        "Safety": "#0046FF",
        "DGMs": "#FF6F3C",
        "Efficient ML": "#03A791"
    }
    if 'tags' in entry.fields:
        for tag in entry.fields['tags'].split(','):
            t = tag.strip()
            bg = tag_colors.get(t, "#888")  # default grey if not found
            s += f""" <span style="background-color:{bg}; color:white; border-radius:4px; padding:2px 6px; font-size:80%; margin-left:4px;">{t}</span>"""

    s += "<br>"

    # ====== Author Line ======
    s += f"""<div style="margin-bottom: 4px;">{generate_person_html(entry.persons['author'], entry.fields['coauthor'])}</div>"""

    # ====== Venue Info ======
    if 'award' in entry.fields.keys():
        s += f"""<span style="font-weight: bold;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <span style="color: blue;">({entry.fields['award']})</span> <br>"""
    else:
        s += f"""<span style="font-weight: bold;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    # ====== Previous Version Info ======
    if 'prev_booktitle' in entry.fields:
        prev_info = f"{entry.fields['prev_booktitle']}"
        if 'prev_year' in entry.fields:
            prev_info += f", {entry.fields['prev_year']}"
        if 'prev_award' in entry.fields:
            s += f"""<span style="color: #888; font-size: 95%;">prelim @ {prev_info}</span> <span style="color: blue;">({entry.fields['prev_award']})</span><br>"""
        else:
            s += f"""<span style="color: #888; font-size: 95%;">prelim @ {prev_info}</span><br>"""

    # ====== Artefacts ======
    artefacts = {'html': '[arXiv]', 'slides': '[slide]', 'code': '[code]', 'video': 'Video', 'poster': 'Poster', 'prjpage': '[Project Page]'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    s += """ </div> </div> </div>"""
    return s


def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': '[slide]', 'video': '[rec]'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_award_entry(entry_key, entry):
    # Safe accessors
    flds = entry.fields
    url = flds.get("html", "#")
    title = flds.get("title", "")
    rank = flds.get("rank", "")
    booktitle = flds.get("booktitle", "")
    year = flds.get("year", "")
    title_color = color.get("title", "#2667ff")

    parts = []
    parts.append('<div class="row mb-3">')

    # Optional image column
    if "img" in flds and flds["img"]:
        parts.append(
            f'<div class="col-sm-3">'
            f'<img src="{flds["img"]}" class="img-fluid img-thumbnail" alt="Project image">'
            f'</div>'
        )
        text_col = "col-sm-9"
    else:
        text_col = "col-sm-12"

    # Text column
    parts.append(f'<div class="{text_col}">')
    parts.append(
        f'<a href="{url}" target="_blank" style="color: {title_color}">{title}</a><br>'
    )
    if rank:
        parts.append(f'{rank} place 🔥<br>')
    parts.append(f'<span style="font-style: italic;">{booktitle}</span>, {year}<br>')

    # Artefacts (optional links)
    artefacts = {
        "slides": "[slide]",
        "video": "Recording",
        "report": "[report]",
        "certificate": "Certificate",
    }
    links = []
    for k, v in artefacts.items():
        if k in flds and flds[k]:
            links.append(f'<a href="{flds[k]}" target="_blank">{v}</a>')
        # else: optionally log a warning if you want

    if links:
        parts.append(" / ".join(links))

    parts.append("</div>")   # close text col
    parts.append("</div>")   # close row

    return "".join(parts)
# def get_award_entry(entry_key, entry):
#     # s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
#     s = """<div style="margin-bottom: 1em;">"""
#     # s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
#     s += """</div><div class="col-sm-9">"""
#     s += f"""<a href="{entry.fields['html']} target="_blank" style="color: {color['title']}">{entry.fields['title']}</a> <br>"""
#     s += f"""{entry.fields['rank']} place 🔥<br>"""
#     s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

#     artefacts = {'slides': 'Slides', 'video': 'Recording', 'report': 'Report', 'certificate': 'Certificate'}
#     i = 0
#     for (k, v) in artefacts.items():
#         if k in entry.fields.keys():
#             if i > 0:
#                 s += ' / '
#             s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
#             i += 1
#         else:
#             print(f'[{entry_key}] Warning: Field {k} missing!')
#     s += """ </div> </div> </div>"""
#     return s

def get_news_html():
    with open('news_list.json', 'r') as f:
        news_entries = json.load(f)

    # 날짜 기준으로 정렬 (최근 것이 위로)
    news_entries.sort(key=lambda e: (e.get("year", 0), e.get("month", 0)), reverse=True)
    s = ""
    for entry in news_entries:
        s += get_news_entry(entry)
    s += '</p>'
    return s


def get_preprints_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('preprint_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_talk_entry(k, bib_data.entries[k])
    return s

def get_awards_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('award_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_award_entry(k, bib_data.entries[k])
    return s

def get_index_html():
    news = get_news_html()
    prep = get_preprints_html()
    pub = get_publications_html()
    talks = get_talks_html()
    awards = get_awards_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <style>
    @media (min-width: 1100px) {{
        .container {{
            max-width: 1200px;
        }}
    }}
    </style>

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-9" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-3" style="width: auto; ">
                        <img src="assets/img/profile.jpg" class="img-thumbnail" width="250px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 2em;">
                    <div class="col-sm-12" style="">
                        <h4>News</h4><hr>
                        {news}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Preprints</h4><hr>
                        {prep}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Publications</h4><hr>
                        {pub}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Awards</h4><hr>
                        {awards}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Talks</h4>
                        <hr>
                        {talks}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
            <div class="col-md-1"></div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')