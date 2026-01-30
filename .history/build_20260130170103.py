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
    <li><span style="color: #dc3545; font-weight: 600;">Safety &amp; Privacy</span> — Ensuring the responsible deployment of generative systems</li>
    <li><span style="color: #6f42c1; font-weight: 600;">Methodologies</span> — Advancing core techniques (sampling methods and new architectures)</li>
    <li><span style="color: #198754; font-weight: 600;">Efficient AI</span> — Optimizing models for real-world deployment under resource constraints</li>
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


def get_paper_entry(entry_key, entry, show_abstract=True):
    fields = entry.fields
    
    # Extract data
    title = fields.get('title', '')
    html_link = fields.get('html', '#')
    img = fields.get('img', '')
    booktitle = fields.get('booktitle', '')
    year = fields.get('year', '')
    award = fields.get('award', None)
    tags = fields.get('tags', '')
    coauthor = fields.get('coauthor', '')
    abstract = fields.get('abstract', '')
    
    # Generate authors HTML
    authors_html = generate_person_html(entry.persons['author'], coauthor)
    
    # Generate tags
    tags_html = get_tag_html(tags)
    
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
    
    s = f'''
    <div class="publication-item">
        <div class="pub-image">
            <img src="{img}" alt="{title}">
        </div>
        <div class="pub-content">
            <div class="pub-title">
                <a href="{html_link}" target="_blank">{title}</a>
                {tags_html}
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


def get_preprints_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('preprint_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
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
        --primary: #1a1a2e;
        --accent: #0066cc;
        --accent-hover: #0052a3;
        --muted: #6c757d;
        --light-bg: #f8f9fa;
        --border: #e9ecef;
        --white: #ffffff;
        --shadow: rgba(0, 0, 0, 0.08);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
        line-height: 1.7;
        color: var(--primary);
        background: linear-gradient(135deg, #fafafa 0%, #f5f7fa 100%);
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
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
        position: sticky;
        top: 0;
        z-index: 1000;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.95);
    }
    
    .nav-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        font-weight: 700;
        font-size: 1.25rem;
        color: var(--primary);
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    
    .nav-links a {
        color: var(--muted);
        font-weight: 500;
        padding: 0.5rem 0;
        position: relative;
    }
    
    .nav-links a:hover,
    .nav-links a.active {
        color: var(--primary);
    }
    
    .nav-links a.active::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent);
        border-radius: 2px;
    }
    
    /* Main Container */
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }
    
    /* Profile Section */
    .profile-section {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 3rem;
        margin-bottom: 4rem;
        align-items: start;
    }
    
    .profile-image {
        position: relative;
    }
    
    .profile-image img {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid var(--white);
        box-shadow: 0 8px 30px var(--shadow);
    }
    
    .profile-info h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: var(--primary);
    }
    
    .profile-info .title {
        font-size: 1.1rem;
        color: var(--muted);
        margin-bottom: 1.5rem;
    }
    
    .profile-info .bio {
        color: #444;
        margin-bottom: 1.5rem;
    }
    
    .profile-info .bio ul {
        margin: 0.75rem 0;
        padding-left: 1.5rem;
    }
    
    .profile-info .bio li {
        margin-bottom: 0.5rem;
    }
    
    .social-links {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .social-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: var(--light-bg);
        border-radius: 6px;
        font-size: 0.9rem;
        color: var(--primary);
        transition: all 0.2s ease;
    }
    
    .social-link:hover {
        background: var(--accent);
        color: var(--white);
    }
    
    /* Section Headers */
    .section {
        margin-bottom: 4rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border);
    }
    
    /* News Section */
    .news-list {
        background: var(--white);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px var(--shadow);
    }
    
    .news-item {
        display: grid;
        grid-template-columns: 100px 1fr;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border);
    }
    
    .news-item:last-child {
        border-bottom: none;
    }
    
    .news-date {
        font-weight: 600;
        color: var(--accent);
        font-size: 0.9rem;
    }
    
    .news-content {
        color: #444;
    }
    
    /* Publication Items */
    .publication-item,
    .talk-item,
    .award-item {
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 1.5rem;
        padding: 1.5rem;
        background: var(--white);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px var(--shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .publication-item:hover,
    .talk-item:hover,
    .award-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .pub-image img,
    .talk-image img,
    .award-image img {
        width: 150px;
        height: 100px;
        object-fit: cover;
        border-radius: 8px;
    }
    
    .pub-title {
        margin-bottom: 0.5rem;
    }
    
    .pub-title a {
        font-weight: 600;
        font-size: 1.05rem;
        color: var(--primary);
    }
    
    .pub-title a:hover {
        color: var(--accent);
    }
    
    .pub-authors {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    
    .pub-authors a {
        color: var(--muted);
    }
    
    .pub-authors a:hover {
        color: var(--accent);
    }
    
    .pub-venue {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.25rem;
    }
    
    .prev-venue {
        font-size: 0.85rem;
        color: var(--muted);
        margin-bottom: 0.25rem;
    }
    
    .award-highlight {
        color: #d63384;
        font-weight: 600;
    }
    
    .pub-links {
        margin-top: 0.5rem;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .paper-link {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: var(--light-bg);
        border-radius: 4px;
        font-size: 0.85rem;
        color: var(--primary);
        transition: all 0.2s ease;
    }
    
    .paper-link:hover {
        background: var(--accent);
        color: var(--white);
    }
    
    /* Research Tags */
    .research-tag {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        color: white;
        font-weight: 500;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    
    /* Talk & Award specific */
    .talk-title,
    .award-title a {
        font-weight: 600;
        font-size: 1.05rem;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }
    
    .talk-venue,
    .award-venue {
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .talk-links,
    .award-links {
        margin-top: 0.5rem;
    }
    
    .award-rank {
        font-size: 1rem;
        font-weight: 600;
        color: #f59e0b;
        margin-bottom: 0.25rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--muted);
        font-size: 0.9rem;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
    }
    
    .footer a {
        color: var(--muted);
    }
    
    .footer a:hover {
        color: var(--accent);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .profile-section {
            grid-template-columns: 1fr;
            text-align: center;
        }
        
        .profile-image {
            display: flex;
            justify-content: center;
        }
        
        .profile-image img {
            width: 160px;
            height: 160px;
        }
        
        .profile-info h1 {
            font-size: 2rem;
        }
        
        .social-links {
            justify-content: center;
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
    prep = get_preprints_html()
    pub = get_publications_html()
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
            <div class="profile-image">
                <img src="assets/img/profile.jpg" alt="{data['name'][0]} {data['name'][1]}">
            </div>
            <div class="profile-info">
                <h1>{data['name'][0]} {data['name'][1]}</h1>
                <p class="title"><strong>{data['title']}</strong><br>{data['affiliation']}</p>
                <div class="bio">
                    {data['bio']}
                </div>
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
            <h2 class="section-header">🏆 Awards</h2>
            {awards}
        </section>
        
        <!-- Talks Section -->
        <section class="section">
            <h2 class="section-header">🎤 Talks</h2>
            {talks}
        </section>
    </div>
    
    <!-- Footer -->
    <footer class="footer">
        <p>© 2025 {data['name'][0]} {data['name'][1]}. Design inspired by <a href="https://yang-song.net/" target="_blank">Yang Song</a>.</p>
    </footer>
    
    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
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
