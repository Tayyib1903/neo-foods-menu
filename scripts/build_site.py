"""Render the public site from Pages CMS JSON. Python standard library only."""
from pathlib import Path
from html import escape
from urllib.parse import unquote
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
MENUS = ('speisekarte', 'getraenkekarte', 'eiskarte')
ASSET_TYPES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.webm', '.pdf', '.css', '.js', '.ico', '.zip'}
ALLERGENS = 'A Gluten · B Krebstiere · C Ei · D Fisch · E Erdnuss · F Soja · G Milch/Laktose · H Schalenfrüchte · L Sellerie · M Senf · N Sesam · O Sulfite · P Lupinen · R Weichtiere'
ARROW = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m14 6-6 6 6 6"/></svg>'
NEXT = '<svg class="ui-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/></svg>'


def text(value):
    return escape(str(value or ''), quote=True)


def lines(value):
    return text(value).replace('\n', '<br>')


def money(value):
    value = str(value).strip()
    if not re.fullmatch(r'\d{1,4},\d{2}', value):
        raise ValueError(f'Ungültiger Preis: {value!r}. Bitte z. B. 5,50 eingeben.')
    return value + ' €'


def asset(root, value, extensions):
    """Only existing repository assets; never execute/render user-provided URLs."""
    path = str(value or '').removeprefix('/neo-foods-menu/').removeprefix('/')
    if not path or '\\' in path or ':' in path or '?' in path or '#' in path:
        raise ValueError(f'Ungültiger Medienpfad: {value!r}')
    path = unquote(path)
    file = (root / path).resolve()
    if not file.is_relative_to(root.resolve()) or not file.is_file() or file.suffix.lower() not in extensions:
        raise ValueError(f'Mediendatei fehlt oder Dateityp unzulässig: {value!r}')
    if file.stat().st_size > 25 * 1024 * 1024:
        raise ValueError(f'Mediendatei über 25 MB: {value!r}. Bitte komprimieren.')
    return text(path)


def enabled(item):
    value = item.get('visible', True)
    if not isinstance(value, bool):
        raise ValueError('Sichtbarkeit muss Ja oder Nein sein.')
    return value


def required(item, key):
    if not isinstance(item.get(key), str) or not item[key].strip():
        raise ValueError(f'Pflichtfeld {key} fehlt.')
    return item[key]


def menu_html(root, slug, data, menus):
    title = text(required(data, 'title'))
    sections = []
    navigation = []
    for i, section in enumerate(data['sections'], 1):
        if not enabled(section):
            continue
        heading = text(required(section, 'title'))
        image = asset(root, section['image'], {'.png', '.jpg', '.jpeg', '.webp', '.gif'})
        navigation.append(f'<a href="#category-{i}">{heading}</a>')
        groups = []
        if slug == 'eiskarte':
            groups.append(f'<p class="scoop-price"><strong>{money(data["scoop_price"])}</strong> pro Kugel</p>')
        for group in section['groups']:
            items = []
            for product in group['items']:
                if not enabled(product):
                    continue
                name = text(required(product, 'name'))
                description = f'<p>{lines(product.get("description"))}</p>' if product.get('description') else ''
                allergens = f'<small>Allergene: {text(product["allergens"])}</small>' if product.get('allergens') else ''
                if slug == 'eiskarte':
                    items.append(f'<li>{name}{description}{allergens}</li>')
                else:
                    price = money(product.get('price'))
                    items.append(f'<article class="product"><div class="product-line"><h4>{name}</h4><strong class="price">{price}</strong></div>{description}{allergens}</article>')
            if items:
                body = ''.join(items)
                if slug == 'eiskarte':
                    body = '<ul class="flavors">' + body + '</ul>'
                groups.append(f'<div class="product-group"><h3>{text(required(group,"title"))}</h3>{body}</div>')
        if section.get('note'):
            groups.append(f'<aside class="milk-note"><h3>{text(section.get("note_title"))}</h3><p>{lines(section["note"])}</p></aside>')
        sections.append(f'<section class="category-section" id="category-{i}" aria-labelledby="heading-{i}"><div class="category-intro"><div><span class="eyebrow">{i:02d} / {title.upper()}</span><h2 id="heading-{i}">{heading}</h2><p>{text(section.get("tagline"))}</p></div><img src="{image}" width="600" height="400" alt="" loading="lazy"></div><div class="product-grid">{"".join(groups)}</div></section>')
    pdf = ''
    if data.get('pdf_visible', True) and data.get('pdf'):
        pdf = f'<a class="pdf-link" href="{asset(root,data["pdf"],{".pdf"})}" download>PDF laden</a>'
    switches = ''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key == slug else '')+f'>{text(menus[key]["title"])}</a>' for key in MENUS)
    logo = '<a class="logo" href="index.html" aria-label="NEO FOODS Startseite"><img src="neo-logo.png" width="110" height="79" alt="NEO FOODS"></a>'
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#103d32"><meta name="description" content="{title} von NEO FOODS Vienna. Alle Produkte und Preise direkt lesen."><title>{title} | NEO FOODS</title><link rel="stylesheet" href="readable-menu.css?v=30"></head><body><a class="skip" href="#menu-content">Zur Karte</a><header class="menu-header"><a href="index.html" class="back">{ARROW}<span>Startseite</span></a>{logo}{pdf}</header><main id="menu-content"><div class="menu-heading"><p class="eyebrow">GUTER GESCHMACK. GUTE MOMENTE.</p><h1>{title}</h1><nav class="menu-switch" aria-label="Unsere Karten">{switches}</nav></div><nav class="category-nav" aria-label="Kategorien">{''.join(navigation)}</nav><div class="menu-content">{''.join(sections)}<details class="allergens"><summary>Allergene &amp; Hinweise</summary><p>{ALLERGENS}</p><p>Weitere Allergene sind je nach Croissantfüllung oder pflanzlicher Milchalternative möglich. Informationen zu Allergenen erhältst du bei unserem Team.</p></details></div></main><footer>{logo}<p>Margaretenplatz 5 · 1050 Wien</p><nav><a href="index.html">Startseite</a><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav></footer></body></html>'''


def home_html(root, menus, offers, moments):
    offer_blocks = []
    for i, offer in enumerate(filter(enabled, offers), 1):
        target = 'aktionen' if i == 1 else f'aktion-{i}'
        subtitle = f'<span>{text(offer.get("subtitle"))}</span>' if offer.get('subtitle') else ''
        time = f'<span class="offer-time">{CLOCK}{text(offer["time"])}</span>' if offer.get('time') else ''
        offer_blocks.append(f'<section class="offer" id="{target}" aria-labelledby="offer-title-{i}"><div class="offer-copy"><p class="eyebrow"><span class="offer-dot" aria-hidden="true"></span>{text(offer.get("label"))}</p><h1 id="offer-title-{i}">{text(required(offer,"title"))} {subtitle}</h1></div><div class="offer-price"><strong>{money(offer["price"])}</strong>{time}</div></section>')
    cards = []
    for i, (slug, ident, label) in enumerate(zip(MENUS, ('speisen','getraenke','eis'), ('SPEISEN','GETRÄNKE','EIS')), 1):
        data = menus[slug]
        image = asset(root, data['sections'][0]['image'], {'.png','.jpg','.jpeg','.webp','.gif'})
        desc = lines(data.get('card_description'))
        if slug == 'eiskarte':
            desc += f'<br><strong>{money(data["scoop_price"])}</strong> pro Kugel'
        cards.append(f'<a class="menu-tile" id="{ident}" href="{slug}.html"><div class="tile-photo"><img src="{image}" alt="" width="600" height="400" loading="lazy"></div><div class="tile-copy"><span class="tile-number">{i:02d} / {label}</span><h3>{text(data["title"])}</h3><p>{desc}</p><span class="tile-cta">Karte öffnen <span class="tile-arrow" aria-hidden="true">{NEXT}</span></span></div></a>')
    films = []
    for i, moment in enumerate(filter(enabled, moments), 1):
        video = asset(root, moment['video'], {'.mp4','.webm'})
        poster = asset(root, moment['poster'], {'.png','.jpg','.jpeg','.webp','.gif'})
        target = 'moments' if i == 1 else f'moment-{i}'
        mime = 'video/webm' if video.endswith('.webm') else 'video/mp4'
        films.append(f'<section class="moments-section moments-feature" id="{target}" aria-labelledby="moments-title-{i}"><div class="moments-copy"><p class="eyebrow">{text(moment.get("label"))}</p><h2 id="moments-title-{i}">{lines(required(moment,"title"))}</h2><p>{lines(moment.get("description"))}</p><div class="social-links"><a href="https://www.instagram.com/neo_foods_vienna/" target="_blank" rel="noopener">Instagram</a><a href="https://www.tiktok.com/@neo_foods_vienna" target="_blank" rel="noopener">TikTok</a></div></div><div class="moments-film"><video controls playsinline preload="metadata" poster="{poster}" aria-label="{text(moment.get("caption"))}"><source src="{video}" type="{mime}"><a href="{video}">Video öffnen</a></video><span>{text(moment.get("caption"))}</span></div></section>')
    template = (root/'templates/index.html').read_text(encoding='utf-8')
    for key, value in {'OFFERS': ''.join(offer_blocks), 'CARDS': ''.join(cards), 'MOMENTS': ''.join(films), 'OFFER_LINK': '<a href="#aktionen">Angebote</a>' if offer_blocks else '', 'MOMENTS_LINK': '<a href="#moments">NEO Moments</a>' if films else ''}.items():
        template = template.replace('{{'+key+'}}', value)
    template = template.replace('home-v10.css?v=27','home-v10.css?v=30')
    if not offer_blocks:
        template = template.replace('<h2 id="menu-title">','<h1 id="menu-title">').replace('Worauf hast du Lust?</h2>','Worauf hast du Lust?</h1>')
    return template


def render(root):
    def load(name):
        return json.loads((root/'content'/f'{name}.json').read_text(encoding='utf-8'))
    menus = {key: load(key) for key in MENUS}
    for key, data in menus.items():
        if not data.get('sections'):
            raise ValueError(f'{key}: Mindestens eine Kategorie ist erforderlich.')
    result = {key+'.html': menu_html(root,key,data,menus) for key,data in menus.items()}
    result['index.html'] = home_html(root,menus,load('offers')['offers'],load('moments')['moments'])
    return result


def build(root=ROOT):
    # Validate all content before touching any output.
    pages = render(root)
    output = root/'_site'
    if output.is_symlink() or output.resolve().parent != root.resolve():
        raise ValueError('_site darf kein symbolischer Link sein.')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    for source in root.iterdir():
        if source.is_file() and not source.is_symlink() and (source.suffix.lower() in ASSET_TYPES or source.suffix=='.html'):
            shutil.copy2(source,output/source.name)
    for folder in ('assets','uploads'):
        if (root/folder).exists():
            for source in (root/folder).rglob('*'):
                if source.is_file() and not source.is_symlink() and source.suffix.lower() in ASSET_TYPES:
                    dest=output/source.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    for name,content in pages.items():
        (output/name).write_text(content,encoding='utf-8')
    (output/'.nojekyll').touch()
    return output


if __name__=='__main__':
    try:
        print(f'Website erstellt: {build()}')
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print(f'Website nicht veröffentlicht: {exc}',file=sys.stderr)
        sys.exit(1)
