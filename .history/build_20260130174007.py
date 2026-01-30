from pybtex.database.input import bibtex
from pybtex.database import parse_file
import json

# Modern color palette inspired by Yang Song's site
colors = {
    'primary': '#1a1a2e',      # Dark navy for text
    'accent': '#0066cc',       # Blue accent for links
    'muted': '#6c757d',        # Muted gray for secondary text
    'light': '#f8f9fa',        # Light background
    'border': '#dee2e6',       # Border color
    'tag_safety': '#dc3545',   # Red for Safety tag
    'tag_dgm': '#6f42c1',      # Purple for DGMs tag
    'tag_efficient': '#198754', # Green for Efficient ML tag
}


def get_personal_data():
    name = ["Dongjae", "Jeon"]
    title = "Master's Student"
    affiliation = "Yonsei University"
    email = "dongjae0324@yonsei.ac.kr"
    scholar = 'https://scholar.google.com/citations?user=SaaN_bAAAAAJ&hl=en'
    github = "https://github.com/Dongjae0324"
    linkedin = "https://www.linkedin.com/in/dongjae-jeon-a74526255"
    cv = "https://dongjae0324.github.io/assets/pdf/CV_dongjae_jeon.pdf"
    
    bio_text = """
I am a first-year master's student in Computer Science at <a href="https://www.yonsei.ac.kr/en_sc/" target="_blank">Yonsei University</a>, 
working in the <a href="https://albert-no.github.io/" target="_blank">Artificial Intelligence and Information Systems Lab</a> 
    with Professor <a href="https://albert-no.github.io/" target="_blank">Albert No</a>.
        
<p style="margin-top: 1em;">I am broadly interested in <strong>generative models</strong>, currently focusing on three specific areas:</p>
        
<ul style="margin-top: 0.5em; padding-left: 1.2em;">
    <li><span style="font-weight: 600;">Safety &amp; Privacy</span> <a href="#pub-1" class="cite-link">[1]</a><a href="#pub-2" class="cite-link">[2]</a><a href="#pub-4" class="cite-link">[4]</a><a href="#pub-7" class="cite-link">[7]</a><a href="#pub-8" class="cite-link">[8]</a></li>
    <li><span style="font-weight: 600;">Methodologies</span> <a href="#pub-1" class="cite-link">[1]</a><a href="#pub-2" class="cite-link">[2]</a><a href="#pub-3" class="cite-link">[3]</a><a href="#pub-5" class="cite-link">[5]</a><a href="#pub-7" class="cite-link">[7]</a></li>
    <li><span style="font-weight: 600;">Efficient AI</span> <a href="#pub-3" class="cite-link">[3]</a><a href="#pub-6" class="cite-link">[6]</a></li>
    </ul>
    
<p style="margin-top: 1em;">I have prior experience in <em>Continual Learning</em> applied to computer vision, specifically Object Detection. 
My primary goal is to deepen our understanding of how machines perceive and, ultimately, leverage that understanding to empower AI for societal good.</p>
"""
    
    return {
        'name': name,
        'title': title,
        'affiliation': affiliation,
        'email': email,
        'scholar': scholar,
        'github': github,
        'linkedin': linkedin,
        'cv': cv,
        'bio': bio_text
    }


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
            
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<strong>{string_part_i}{star}</strong>'
        elif string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}{star}</a>'
        else:
            string_part_i = f'{string_part_i}{star}'
            
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s


def get_venue_badge(booktitle, award=None):
    """Generate venue badge with optional award highlight"""
    venue_colors = {
        'ICML': '#e74c3c',
        'NeurIPS': '#9b59b6', 
        'ICLR': '#3498db',
        'CVPR': '#27ae60',
        'ICCV': '#f39c12',
        'ECCV': '#1abc9c',
        'AAAI': '#e91e63',
        'ACL': '#00bcd4',
    }
    
    # Extract venue name
    venue_name = booktitle.split()[0] if booktitle else ""
    badge_color = venue_colors.get(venue_name, '#6c757d')
    
    badge = f'<span class="venue-badge" style="background-color: {badge_color};">{booktitle}</span>'
    
    if award:
        badge += f' <span class="award-badge">{award}</span>'
    
    return badge


def get_tag_html(tags_str):
    """Generate colored tags for research areas"""
    if not tags_str:
        return ""
    
    tag_colors = {
        "Safety": colors['tag_safety'],
        "DGMs": colors['tag_dgm'],
        "Efficient ML": colors['tag_efficient']
    }
    
    html = ""
    for tag in tags_str.split(','):
        t = tag.strip()
        bg = tag_colors.get(t, "#6c757d")
        html += f'<span class="research-tag" style="background-color: {bg};">{t}</span>'
    
    return html


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

    date_str = f"{month_name} {year}" if month_name and year else str(year)
    
    return f'''
    <div class="news-item">
        <span class="news-date">{date_str}</span>
        <span class="news-content">{content}</span>
    </div>
    '''


def get_paper_entry(entry_key, entry, paper_num=None):
    fields = entry.fields
    
    # Extract data
    title = fields.get('title', '')
    html_link = fields.get('html', '#')
    img = fields.get('img', '')
    booktitle = fields.get('booktitle', '')
    year = fields.get('year', '')
    award = fields.get('award', None)
    coauthor = fields.get('coauthor', '')
    
    # Generate authors HTML
    authors_html = generate_person_html(entry.persons['author'], coauthor)
    
    # Generate links
    links = []
    if 'html' in fields:
        links.append(f'<a href="{fields["html"]}" target="_blank" class="paper-link">arXiv</a>')
    if 'code' in fields:
        links.append(f'<a href="{fields["code"]}" target="_blank" class="paper-link">Code</a>')
    if 'prjpage' in fields:
        links.append(f'<a href="{fields["prjpage"]}" target="_blank" class="paper-link">Project</a>')
    if 'slides' in fields:
        links.append(f'<a href="{fields["slides"]}" target="_blank" class="paper-link">Slides</a>')
    if 'video' in fields:
        links.append(f'<a href="{fields["video"]}" target="_blank" class="paper-link">Video</a>')
    
    links_html = ' '.join(links)
    
    # Award/Venue info
    venue_info = f'<em>{booktitle}</em>, {year}'
    if award:
        venue_info += f' <span class="award-highlight">({award})</span>'
    
    # Previous version info
    prev_info = ""
    if 'prev_booktitle' in fields:
        prev_text = f"{fields['prev_booktitle']}"
        if 'prev_year' in fields:
            prev_text += f", {fields['prev_year']}"
        if 'prev_award' in fields:
            prev_info = f'<div class="prev-venue">Previously at {prev_text} <span class="award-highlight">({fields["prev_award"]})</span></div>'
        else:
            prev_info = f'<div class="prev-venue">Previously at {prev_text}</div>'
    
    # Paper ID for citation linking
    paper_id = f'id="pub-{paper_num}"' if paper_num else ''
    num_label = f'<span class="pub-num">[{paper_num}]</span> ' if paper_num else ''
    
    s = f'''
    <div class="publication-item" {paper_id}>
        <div class="pub-image">
            <img src="{img}" alt="{title}">
        </div>
        <div class="pub-content">
            <div class="pub-title">
                <a href="{html_link}" target="_blank">{title}</a> {num_label}
            </div>
            <div class="pub-authors">{authors_html}</div>
            <div class="pub-venue">{venue_info}</div>
            {prev_info}
            <div class="pub-links">{links_html}</div>
        </div>
    </div>
    '''
    
    return s


def get_talk_entry(entry_key, entry):
    fields = entry.fields
    
    title = fields.get('title', '')
    booktitle = fields.get('booktitle', '')
    year = fields.get('year', '')
    img = fields.get('img', '')
    
    links = []
    if 'slides' in fields:
        links.append(f'<a href="{fields["slides"]}" target="_blank" class="paper-link">Slides</a>')
    if 'video' in fields:
        links.append(f'<a href="{fields["video"]}" target="_blank" class="paper-link">Recording</a>')
    
    links_html = ' '.join(links)
    
    return f'''
    <div class="talk-item">
        <div class="talk-image">
            <img src="{img}" alt="{title}">
        </div>
        <div class="talk-content">
            <div class="talk-title">{title}</div>
            <div class="talk-venue"><em>{booktitle}</em>, {year}</div>
            <div class="talk-links">{links_html}</div>
        </div>
    </div>
    '''


def get_award_entry(entry_key, entry):
    fields = entry.fields
    
    url = fields.get("html", "#")
    title = fields.get("title", "")
    rank = fields.get("rank", "")
    booktitle = fields.get("booktitle", "")
    year = fields.get("year", "")
    img = fields.get("img", "")
    
    links = []
    if 'slides' in fields:
        links.append(f'<a href="{fields["slides"]}" target="_blank" class="paper-link">Slides</a>')
    if 'report' in fields:
        links.append(f'<a href="{fields["report"]}" target="_blank" class="paper-link">Report</a>')
    
    links_html = ' '.join(links)
    
    rank_emoji = "🥇" if rank == "1st" else "🥈" if rank == "2nd" else "🥉" if rank == "3rd" else "🏆"
    
    return f'''
    <div class="award-item">
        <div class="award-image">
            <img src="{img}" alt="{title}">
        </div>
        <div class="award-content">
            <div class="award-title">
                <a href="{url}" target="_blank">{title}</a>
            </div>
            <div class="award-rank">{rank_emoji} {rank} Place</div>
            <div class="award-venue"><em>{booktitle}</em>, {year}</div>
            <div class="award-links">{links_html}</div>
        </div>
    </div>
    '''


def get_news_html():
    with open('news_list.json', 'r') as f:
        news_entries = json.load(f)

    news_entries.sort(key=lambda e: (e.get("year", 0), e.get("month", 0)), reverse=True)
    
    s = '<div class="news-list">'
    for entry in news_entries[:8]:  # Show only recent 8 news items
        s += get_news_entry(entry)
    s += '</div>'
    
    return s


def get_preprints_html(start_num=1):
    parser = bibtex.Parser()
    bib_data = parser.parse_file('preprint_list.bib')
    keys = list(bib_data.entries.keys())
    s = ""
    for i, k in enumerate(keys):
        s += get_paper_entry(k, bib_data.entries[k], paper_num=start_num + i)
    return s, len(keys)


def get_publications_html(start_num=1):
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = list(bib_data.entries.keys())
    s = ""
    for i, k in enumerate(keys):
        s += get_paper_entry(k, bib_data.entries[k], paper_num=start_num + i)
    return s


def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_talk_entry(k, bib_data.entries[k])
    return s


def get_awards_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('award_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_award_entry(k, bib_data.entries[k])
    return s


def get_css():
    return '''
    :root {
        --primary: #222;
        --accent: #0066cc;
        --accent-hover: #004499;
        --muted: #555;
        --light-bg: #f5f5f5;
        --border: #ddd;
        --white: #ffffff;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-size: 14px;
        line-height: 1.5;
        color: var(--primary);
        background: var(--white);
        min-height: 100vh;
    }
    
    a {
        color: var(--accent);
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: var(--accent-hover);
    }
    
    /* Navigation */
    .navbar {
        background: var(--white);
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--primary);
    }
    
    .nav-links {
        display: flex;
        gap: 1.5rem;
    }
    
    .nav-links a {
        color: var(--muted);
        font-size: 0.95rem;
    }
    
    .nav-links a:hover,
    .nav-links a.active {
        color: var(--accent);
    }
    
    /* Main Container */
    .container {
        max-width: 850px;
        margin: 0 auto;
        padding: 2rem 2rem;
    }
    
    /* Profile Section */
    .profile-section {
        margin-bottom: 2.5rem;
    }
    
    .profile-header {
        display: grid;
        grid-template-columns: 160px 1fr;
        gap: 2rem;
        margin-bottom: 1.5rem;
        align-items: start;
    }
    
    .profile-image {
        position: relative;
    }
    
    .profile-image img {
        width: 160px;
        height: auto;
        border: 1px solid var(--border);
    }
    
    .profile-info h1 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        color: var(--primary);
    }
    
    .profile-info .title {
        font-size: 0.875rem;
        color: var(--muted);
        margin-bottom: 0.75rem;
        line-height: 1.4;
    }
    
    .social-links {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        font-size: 0.8rem;
    }
    
    .social-link {
        color: var(--accent);
    }
    
    .social-link:hover {
        text-decoration: underline;
    }
    
    .social-link i {
        margin-right: 0.25rem;
    }
    
    /* Bio Section */
    .bio-section {
        color: var(--primary);
        line-height: 1.7;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
    
    .bio-section p {
        margin-bottom: 0.75rem;
    }
    
    .bio-section ul {
        margin: 0.5rem 0 0.75rem 0;
        padding-left: 1.25rem;
    }
    
    .bio-section li {
        margin-bottom: 0.35rem;
    }
    
    /* Section Headers */
    .section {
        margin-bottom: 2rem;
    }
    
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--border);
    }
    
    /* News Section */
    .news-list {
        font-size: 0.85rem;
    }
    
    .news-item {
        display: grid;
        grid-template-columns: 75px 1fr;
        gap: 0.5rem;
        padding: 0.25rem 0;
    }
    
    .news-date {
        font-weight: 600;
        color: var(--primary);
        font-size: 0.8rem;
    }
    
    .news-content {
        color: var(--primary);
    }
    
    /* Publication Items */
    .publication-item,
    .talk-item,
    .award-item {
        display: grid;
        grid-template-columns: 140px 1fr;
        gap: 1.25rem;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    
    .publication-item {
        display: flex;
        gap: 20px;
        margin-bottom: 10px;
        margin-left: 10px;
    }
    .talk-item:last-child,
    .award-item:last-child {
        border-bottom: none;
    }

    .pub-image img {
    width: 160px; /* or your preferred size */
    height: auto;
    }

    .talk-image img,
    .award-image img {
        width: 140px;
        height: 95px;
        object-fit: cover;
        border: 1px solid var(--border);
    }
    
    .pub-title {
        margin-bottom: 0.25rem;
    }
    
    .pub-num {
        color: var(--muted);
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .pub-title a {
        font-weight: 500;
        font-size: 0.9rem;
        color: var(--accent);
    }
    
    .pub-title a:hover {
        text-decoration: underline;
    }
    
    /* Citation links in bio */
    .cite-link {
        color: var(--accent);
        font-size: 0.8rem;
        margin-left: 0.1rem;
    }
    
    .cite-link:hover {
        text-decoration: underline;
    }
    
    /* Highlight effect when paper is targeted */
    .publication-item:target {
        background-color: #fffde7;
        border-left: 3px solid var(--accent);
        padding-left: calc(1rem - 3px);
        margin-left: -3px;
    }
    
    .publication-item {
        transition: background-color 0.3s ease;
        scroll-margin-top: 80px;
    }
    
    .pub-authors {
        color: var(--muted);
        font-size: 0.8rem;
        margin-bottom: 0.15rem;
    }
    
    .pub-authors a {
        color: var(--muted);
    }
    
    .pub-authors a:hover {
        color: var(--accent);
    }
    
    .pub-venue {
        font-size: 0.8rem;
        color: var(--muted);
        margin-bottom: 0.15rem;
    }
    
    .prev-venue {
        font-size: 0.75rem;
        color: var(--muted);
        margin-bottom: 0.15rem;
    }
    
    .award-highlight {
        color: #c00;
        font-weight: 600;
    }
    
    .pub-links {
        margin-top: 0.25rem;
        font-size: 0.75rem;
    }
    
    .paper-link {
        color: var(--accent);
        margin-right: 0.5rem;
    }
    
    .paper-link:hover {
        text-decoration: underline;
    }
    
    .paper-link::before {
        content: '[';
    }
    
    .paper-link::after {
        content: ']';
    }
    
    /* Research Tags */
    .research-tag {
        display: inline-block;
        padding: 0.1rem 0.4rem;
        border-radius: 2px;
        font-size: 0.7rem;
        color: white;
        font-weight: 500;
        margin-left: 0.4rem;
        vertical-align: middle;
    }
    
    /* Talk & Award specific */
    .talk-title,
    .award-title a {
        font-weight: 500;
        font-size: 1rem;
        color: var(--accent);
        margin-bottom: 0.2rem;
    }
    
    .award-title a:hover {
        text-decoration: underline;
    }
    
    .talk-venue,
    .award-venue {
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    
    .talk-links,
    .award-links {
        margin-top: 0.35rem;
        font-size: 0.85rem;
    }
    
    .award-rank {
        font-size: 0.95rem;
        font-weight: 600;
        color: #c00;
        margin-bottom: 0.2rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: var(--muted);
        font-size: 0.85rem;
        border-top: 1px solid var(--border);
        margin-top: 2rem;
    }
    
    .footer a {
        color: var(--muted);
    }
    
    .footer a:hover {
        color: var(--accent);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .profile-header {
            grid-template-columns: 1fr;
            text-align: center;
            gap: 1rem;
        }
        
        .profile-image {
            display: flex;
            justify-content: center;
        }
        
        .profile-image img {
            width: 140px;
        }
        
        .profile-info h1 {
            font-size: 1.8rem;
        }
        
        .social-links {
            justify-content: center;
        }
        
        .bio-section {
            text-align: left;
        }
        
        .publication-item,
        .talk-item,
        .award-item {
            grid-template-columns: 1fr;
        }
        
        .pub-image,
        .talk-image,
        .award-image {
            display: flex;
            justify-content: center;
        }
        
        .pub-image img,
        .talk-image img,
        .award-image img {
            width: 100%;
            max-width: 300px;
            height: auto;
        }
        
        .news-item {
            grid-template-columns: 1fr;
            gap: 0.25rem;
        }
        
        .nav-links {
            gap: 1rem;
        }
    }
    '''


def get_index_html():
    data = get_personal_data()
    news = get_news_html()
    prep, prep_count = get_preprints_html(start_num=1)
    pub = get_publications_html(start_num=prep_count + 1)
    talks = get_talks_html()
    awards = get_awards_html()
    css = get_css()
    
    s = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name'][0]} {data['name'][1]}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
    {css}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#" class="nav-brand">{data['name'][0]} {data['name'][1]}</a>
            <div class="nav-links">
                <a href="#about" class="active">About</a>
                <a href="#publications">Publications</a>
                <a href="#awards">Awards</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <!-- Profile Section -->
        <section id="about" class="profile-section">
            <div class="profile-header">
                <div class="profile-image">
                    <img src="assets/img/profile.jpg" alt="{data['name'][0]} {data['name'][1]}">
                </div>
                <div class="profile-info">
                    <h1>{data['name'][0]} {data['name'][1]}</h1>
                    <p class="title"><strong>{data['title']}</strong><br>{data['affiliation']}</p>
                    <div class="social-links">
                        <a href="{data['cv']}" target="_blank" class="social-link">
                            <i class="fa-solid fa-file-pdf"></i> CV
                        </a>
                        <a href="mailto:{data['email']}" class="social-link">
                            <i class="fa-solid fa-envelope"></i> Email
                        </a>
                        <a href="{data['scholar']}" target="_blank" class="social-link">
                            <i class="fa-solid fa-graduation-cap"></i> Scholar
                        </a>
                        <a href="{data['github']}" target="_blank" class="social-link">
                            <i class="fa-brands fa-github"></i> GitHub
                        </a>
                        <a href="{data['linkedin']}" target="_blank" class="social-link">
                            <i class="fa-brands fa-linkedin"></i> LinkedIn
                        </a>
                    </div>
                </div>
                    </div>
            <div class="bio-section">
                {data['bio']}
                </div>
        </section>
        
        <!-- News Section -->
        <section class="section">
            <h2 class="section-header">News</h2>
            {news}
        </section>
        
        <!-- Selected Publications -->
        <section id="publications" class="section">
            <h2 class="section-header">Publications</h2>
            <p style="color: var(--muted); margin-bottom: 1.5rem; font-size: 0.95rem;">
                (*) denotes equal contribution
            </p>
            
            <h3 style="font-size: 1.1rem; color: var(--muted); margin-bottom: 1rem; font-weight: 600;">Preprints</h3>
            {prep}
            
            <h3 style="font-size: 1.1rem; color: var(--muted); margin: 2rem 0 1rem; font-weight: 600;">Peer-Reviewed</h3>
                        {pub}
        </section>
        
        <!-- Awards Section -->
        <section id="awards" class="section">
            <h2 class="section-header">Awards</h2>
                        {awards}
        </section>
        
        <!-- Talks Section -->
        <section class="section">
            <h2 class="section-header">Talks</h2>
                        {talks}
        </section>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <p>© 2026 {data['name'][0]} {data['name'][1]}.</p>
    </footer>
    
    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                    // Update URL hash without jumping
                    history.pushState(null, null, targetId);
                    
                    // Add highlight flash for publication items
                    if (target.classList.contains('publication-item')) {{
                        target.style.backgroundColor = '#fff9c4';
                        setTimeout(() => {{
                            target.style.backgroundColor = '';
                        }}, 1500);
                    }}
                }}
            }});
        }});
        
        // Update active nav link on scroll
        window.addEventListener('scroll', () => {{
            const sections = document.querySelectorAll('section[id]');
            const navLinks = document.querySelectorAll('.nav-links a');
            
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 200) {{
                    current = section.getAttribute('id');
                }}
            }});
            
            navLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});
        
        // Handle direct URL hash on page load
        if (window.location.hash) {{
            const target = document.querySelector(window.location.hash);
            if (target && target.classList.contains('publication-item')) {{
                setTimeout(() => {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    target.style.backgroundColor = '#fff9c4';
                    setTimeout(() => {{ target.style.backgroundColor = ''; }}, 1500);
                }}, 100);
            }}
        }}
    </script>
</body>
</html>
'''
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')


if __name__ == '__main__':
    write_index_html('index.html')
