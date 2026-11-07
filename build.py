#!/usr/bin/env python3
"""Static site generator for the Heidi Gubbins redesign.
Run:  python3 build.py   → writes HTML into ./site
Serve: python3 -m http.server -d site 8080
"""
import json, os, re, html
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SITE = ROOT / "site"
IMG = SITE / "assets" / "img"
manifest = json.loads((IMG / "manifest.json").read_text())
_dims = {}

def webp(name):
    """manifest names are .jpg/.jpeg/.png; we serve .webp for photos."""
    base = re.sub(r"\.(jpe?g)$", "", name, flags=re.I)
    return base + ".webp" if not name.lower().endswith(".png") else name

def dims(f):
    if f not in _dims:
        try:
            with Image.open(IMG / f) as im: _dims[f] = im.size
        except Exception: _dims[f] = (1600, 1200)
    return _dims[f]

def img(R, name, alt="", eager=False, cls=""):
    f = webp(name if "." in name else name + ".jpg")
    w, h = dims(f)
    return (f'<img src="{R}assets/img/{f}" alt="{html.escape(alt)}" width="{w}" height="{h}"'
            f'{" fetchpriority=high" if eager else " loading=lazy"} decoding="async"{f" class={cls!r}" if cls else ""}>')

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
CONTACT = dict(
    address="Av. Blvd. Príncipe Alfonso de Hohenlohe<br>Marbella Real 20 &amp; 21, The Golden Mile<br>29602 Marbella, Spain",
    map="https://maps.app.goo.gl/ymoVG6Hj6spyPFpo9",
    tel_clients="+34 673 63 81 35", tel_clients_raw="+34673638135",
    tel_supply="+34 637 077 836", tel_supply_raw="+34637077836",
    email="contact@heidigubbins.com", orders="orders@heidigubbins.com", press="marketing@heidigubbins.com",
)
SOCIAL = [("Instagram", "https://www.instagram.com/heidi.gubbins/"), ("Facebook", "https://m.facebook.com/HeidiGubbinsInteriorDesign"),
          ("YouTube", "https://m.youtube.com/@HeidiGubbinsInteriorDesigner"), ("LinkedIn", "https://es.linkedin.com/in/heidi-gubbins-36233a144")]

NAV = [
    ("The Studio", "studio/", "2024-12-the-studio-heidi-gubbins-interior-design-marbella-1.jpg"),
    ("Heidi Gubbins", "heidi-gubbins/", "2025-07-heidi1.jpg"),
    ("Projects", "projects/", "2025-02-heidi-gubbins-galatea-2-hd-27.jpg"),
    ("Boutique", "boutique/", "2025-02-chair.jpg"),
    ("Design Stories", "design-stories/", "2025-07-design-stories-2-scaled.jpg"),
    ("Press", "press/", "2025-06-press-june25.jpg"),
    ("Contact", "contact/", "2021-09-contact-heidi-gubbins-interior-design-marbella.jpg"),
]

def gal(slug, skip_feature=True):
    out = []
    for f in manifest["projects"].get(slug, []):
        if skip_feature and re.search(r"2024-05-.*feature", f): continue
        if f.endswith(".png"): continue
        out.append(f)
    return out

PROJECTS = [
    dict(slug="casa-vero", title="Casa Vero", loc="Marbella", type="Private Residence", cat="residential",
         cover="2025-02-heidi-gubbins-galatea-2-hd-27.jpg",
         lead="A home shaped around an effervescent personality — whimsical and artistic, yet inherently calm.",
         body=["Casa Vero was conceived as a portrait of its owner: her warmth, her strength and her love of family and entertaining. A quiet, neutral foundation lets bold artistic gestures take the lead.",
               "Large-scale murals and curated art borrow their hues from nature and the slow tones of sunset. In the cinema room a textured dark leather wall sets an immersive mood, arching murals extend the story, and playful upholstery keeps sophistication and joy in balance."]),
    dict(slug="tower-view-penthouse", title="Tower-View Penthouse", loc="Marbella", type="Penthouse", cat="residential",
         cover="2024-03-project-1.jpg",
         lead="A penthouse completely reimagined around the Roman watchtower that stands in its garden, gazing out to sea.",
         body=["Raw, textured materials and bespoke panelling build a natural, immersive atmosphere, each surface contributing to a narrative composed with precision.",
               "Light is orchestrated to envelop the double-height lounge, crowned by a choreography of pendants and a countryside-style fireplace. In the bathrooms, noble materials and expansive stone slabs turn function into indulgence."]),
    dict(slug="boho-wellness", title="Boho Wellness", loc="Boho Club, Marbella", type="Spa & Wellness", cat="commercial", award="Award — Best Luxury Spa",
         cover="2024-12-ashiana-project-featured.jpg",
         lead="A sensorial journey through nature — a spa conceived to rejuvenate body and spirit.",
         body=["At the heart of Boho Club on the Golden Mile, the wellness centre embodies the brand’s eclectic spirit while establishing an identity entirely its own.",
               "Each experience room carries a different element of nature — pastel murals that evoke freedom, water-inspired materials that recall the ocean, finishes that move from rough to lustrous. From the Cocoon Room to the Oyster Room and the enveloping Cave, every space tells its own story, with murals and artwork crafted alongside local artisans."]),
    dict(slug="bongo", title="Bongo", loc="Granada", type="Restaurant & Bar", cat="commercial",
         cover="2024-01-1-portfolio-bongo.jpg",
         lead="A secret artistic cave — eccentric elegance and dramatic flair within existing structural limits.",
         body=["Dark palettes punctuated by colour, hand-painted prehistoric-inspired ceilings and strategic lighting create a deeply sensorial venue. Low mezzanine ceilings intensify the cave effect, with mirrors adding depth and a DJ booth uniting dining and entertainment.",
               "Below, neon hues pour from the ceiling, contrasting organic painted walls, industrial finishes and a golden elevator — themes and textures mixed into an identity of its own."]),
    dict(slug="deep-access", title="Deep Access", loc="Guadalmina", type="Villa", cat="residential",
         cover="2024-01-2-portfolio-deep-access.jpg",
         lead="Earthy neutrals, solid materials and intricate details — a sense of depth that evokes deep-sea diving.",
         body=["A transcendental space where masculine, sculptural furniture is balanced by playful details that create movement and visual engagement throughout the home."]),
    dict(slug="coral-cabana", title="Coral & Cabana", loc="Marbella", type="Seaside Residence", cat="residential",
         cover="2024-02-main-portfolio-coral-cabana.jpg",
         lead="Raw elegance and the feeling of a golden-hour afternoon by the beach.",
         body=["Organic textures and delicate materials pay tribute to a setting of greenery between sea and mountains. A shoal of sculptural lights animates the double-height lounge; the wine cellar is lined in irregular stone for an authentic cavern feel.",
               "Monochrome patterns, coral hues and tan accents dress the soft furnishings, while weave-like walls in the master bedroom quietly recall beach cabanas."]),
    dict(slug="coastal-rarity", title="Coastal Rarity", loc="Cortijo Blanco, Marbella", type="Beachside Villa", cat="residential",
         cover="2024-02-main-portfolio-coastal-rarity.jpg",
         lead="A peaceful coastal retreat where curved forms soften modern Andalusian architecture.",
         body=["Natural cladding forms an organic backdrop for light furnishings, ethnic pieces, 70s-inspired furniture and Art Deco touches. Tramoto granite, Terra Larix wood, smoked glass and brass detailing counterpoint the villa’s clean lines.",
               "The master bedroom takes its cue from the whale — tranquil, romantic and cocooning, layered with aged mirrors, Tibetan lambswool and soft leathers."]),
    dict(slug="scaled-rapture", title="Scaled Rapture", loc="Marbella", type="Villa", cat="residential",
         cover="2024-02-main-portfolio-scaled-rapture.jpg",
         lead="Sophisticated and eclectic — a love for the abstract, at grand scale.",
         body=["Double-height ceilings call for sizeable pieces that bring drama and grandeur, while smaller rooms reveal a softer side through light wood cladding and delicate detail."]),
    dict(slug="the-contemporary-tree-house", title="The Contemporary Tree House", loc="El Madroñal", type="Villa", cat="residential",
         cover="2024-02-main-portfolio-the-contemporary-tree-house.jpg",
         lead="Minimalist architecture brought into conversation with the wooded hills above Marbella.",
         body=["Organic shapes, rustic tones and natural greens compose an ode to the landscape. The fireplace is finished in corroded metal and angled partitions to bring intimacy to an open plan.",
               "The master bedroom draws on the façade of Casa Lleó i Morera in Barcelona — grey and sand stone, aged brass, ebony-toned wood and delicate pink — joined by motifs of the Sakura cherry blossom."]),
    dict(slug="canoe-inspired", title="Canoe Inspired", loc="Sotogrande", type="Lounge", cat="residential",
         cover="2024-02-main-portfolio-canoe-inspired.jpg",
         lead="Tone-on-tone nude hues, rich texture and the quiet image of a floating canoe.",
         body=["A minimalist approach compensated by a wealth of texture. A patterned rug in blues and coral dresses the floor while a hand-painted black-and-white ceiling completes the composition — the perfect place to settle by the fire."]),
    dict(slug="once-upon-a-time-in-miami", title="Once Upon a Time in Miami", loc="Miami", type="Lounge", cat="residential",
         cover="2024-02-main-portfolio-once-upon-a-time-in-miami.jpg",
         lead="An elegant, informal lounge beneath cascading, ethereal light.",
         body=["Versatile seating compositions fill the generous volume, while corroded copper cladding and wood-slatted walls wrap contemporary furniture that looks out over the pool deck."]),
    dict(slug="the-view-from-here", title="The View From Here", loc="Cortijo Blanco, Marbella", type="Beachside Residence", cat="residential",
         cover="2024-02-main-portfolio-the-view-from-here.jpg",
         lead="La Concha mountain — and the panorama from its summit — reinterpreted as interior.",
         body=["Irregular, sculpted and voluminous forms echo the coastline stretching towards Gibraltar and North Africa. A light, earthy palette and vintage pieces celebrate an unequalled setting."]),
    dict(slug="biloba", title="Biloba", loc="Granada", type="Tapas Bar", cat="commercial",
         cover="2024-02-main-portfolio-biloba.jpg",
         lead="Contrast and decorative daring for a venue designed to be seen — and entered.",
         body=["An aqua-blue distressed wall cladding sets the tone for brass, oxidised metals and vibrant blue glass. The ceiling was raised on brass-toned trusses and windows enlarged to frame the town.",
               "Chandeliers, Chesterfield upholstery and textured oak meet a stand-up bar that opens onto the esplanade, while a distressed lime-yellow door issues the final invitation."]),
    dict(slug="sweet-carolina", title="Sweet Carolina", loc="Marbella", type="Refurbishment", cat="refurbishment",
         cover="2024-02-main-portfolio-sweet-carolina.jpg",
         lead="A dark, dated Spanish home transformed into contemporary-chic country — without moving a single wall.",
         body=["Walls and ceilings were stripped, beams repainted in a deep tone against white, and a new kitchen designed to overcome low ceilings, with a breakfast corner for the family.",
               "Stone slabs chosen for their veining meet daring solid-brass doors; every furnishing and light was designed for the home and fits it like a glove."]),
    dict(slug="the-oasis-penthouse", title="The Oasis Penthouse", loc="Marbella", type="Show Home", cat="residential",
         cover="2024-02-main-portfolio-the-oasis-penthouse.jpg",
         lead="A show home that inspires — light, earthy and memorable.",
         body=["Natural wood cladding, organic soft furnishings and handcrafted wall textures by local artisans, enlivened with playful murals — because a show home should be remembered."]),
    dict(slug="real-de-la-quinta", title="Rock Solid", loc="Real de la Quinta, Marbella", type="Penthouse", cat="residential",
         cover="2024-02-main-portfolio-rock-solid.jpg",
         lead="A contemporary holiday home where form follows function — and the sea view leads.",
         body=["Greens, greys and wood accents, with dramatically arranged lamps as the statement in each principal space — aesthetics guided by practical considerations."]),
    dict(slug="tranquil-abode", title="Tranquil Abode", loc="Sierra Blanca, Marbella", type="Villa", cat="residential",
         cover=None,
         lead="A narrative inspired by nature’s allure in the hills of Camoján.",
         body=["A waterfall-inspired chimney, a dining room like a forest stroll, and a domed primary bedroom wrapped in seamless natural texture.",
               "Organic shapes, wood, glass and stone converge into a luxurious ambience where asymmetry and carefully chosen art create intimacy."]),
    dict(slug="royal-aloha-suites", title="Barefoot at a Pied-à-Terre", loc="Nueva Andalucía, Marbella", type="Apartment", cat="residential",
         cover="2024-03-featured.jpg",
         lead="An ethos of natural simplicity — ease, intimacy and light.",
         body=["Lofty doors, impactful art and a sleek black lamp tune the scale of the living room; smoky-glass cabinetry reflects natural light through the lounge.",
               "Translucent dividers dissolve boundaries, and a sliding glass wall brings a garden-like allure from bath to bed."]),
]
for p in PROJECTS:
    p["gallery"] = gal(p["slug"])
    if not p["cover"]: p["cover"] = p["gallery"][0]
CATS = {"residential": "Residential", "commercial": "Commercial", "refurbishment": "Refurbishment"}

SERVICES = ["Residential Interior Design", "Commercial Interior Design", "Refurbishment & Renovations", "Architecture", "Show Homes",
            "Digital Home Staging", "Project Consultation & Planning", "Bespoke Furniture", "Lighting", "Outdoor Furniture", "Kitchens",
            "Bathrooms", "Landscaping", "Soft Furnishings", "Art", "Accessories", "CAD Drawings", "3D Renderings"]

# 1px line icons for each service (32×32 grid, drawn on hover via stroke-dashoffset)
SERVICE_ICONS = [
    "M5 15 L16 6 L27 15 M8 13 V26 H24 V13 M13 26 V19 H19 V26",
    "M6 27 V8 H26 V27 M4 27 H28 M10 12 H13 M19 12 H22 M10 17 H13 M19 17 H22 M14 27 V21 H18 V27",
    "M6 6 H22 V12 H6 Z M22 9 H26 V16 H15 V20 M13 20 H17 V28 H13 Z",
    "M14 7 a2 2 0 1 0 4 0 a2 2 0 1 0 -4 0 M16 3 V5 M15 9 L8 28 M17 9 L24 28 M11 20 Q16 23 21 20",
    "M5 16 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 M15 16 H28 M23 16 V20 M27 16 V19",
    "M4 6 H28 V22 H4 Z M12 27 H20 M16 22 V27 M10 18 V14 H22 V18 M8 18 H24",
    "M9 6 H23 V28 H9 Z M13 4 H19 V8 H13 Z M12 15 L14 17 L19 12 M12 22 H20",
    "M8 13 V9 Q8 6 11 6 H21 Q24 6 24 9 V13 M5 22 V14 Q5 12 7 12 Q9 12 9 14 V18 H23 V14 Q23 12 25 12 Q27 12 27 14 V22 Z M8 22 V26 M24 22 V26",
    "M16 3 V10 M10 18 Q10 10 16 10 Q22 10 22 18 Z M14 22 Q16 24 18 22",
    "M4 14 Q16 2 28 14 Z M16 14 V28 M11 28 H21",
    "M7 13 H25 V23 Q25 26 22 26 H10 Q7 26 7 23 Z M4 13 H28 M13 10 Q13 7 16 7 Q19 7 19 10 M16 4 V7",
    "M4 16 H28 V19 Q28 25 22 25 H10 Q4 25 4 19 Z M7 16 V7 Q7 5 9 5 Q11 5 11 7 M10 25 L9 28 M22 25 L23 28",
    "M6 26 Q6 8 26 6 Q24 26 6 26 Z M6 26 L18 14",
    "M6 8 Q16 11 26 8 Q23 16 26 24 Q16 21 6 24 Q9 16 6 8 Z M11 16 Q16 18 21 16",
    "M5 6 H27 V26 H5 Z M8 23 L14 15 L18 20 L21 17 L25 23 Z M20 11 a1.5 1.5 0 1 0 3 0 a1.5 1.5 0 1 0 -3 0",
    "M13 4 H19 M14 4 V9 Q8 13 8 20 Q8 28 16 28 Q24 28 24 20 Q24 13 18 9 V4",
    "M5 27 V5 L27 27 Z M10 22 V17 L15 22 Z M5 10 H8 M5 15 H8 M5 20 H7",
    "M16 4 L27 10 V22 L16 28 L5 22 V10 Z M5 10 L16 16 L27 10 M16 16 V28",
]

def services_list(cls="c-6-7"):
    li = "".join(
        f'<li><span class="svc-name">{esc(s)}</span>'
        f'<svg class="svc-ico" viewBox="0 0 32 32" aria-hidden="true"><path d="{d}" pathLength="1"/></svg></li>'
        for s, d in zip(SERVICES, SERVICE_ICONS))
    return f'<ul class="services {cls}" data-reveal>{li}</ul>'

DISCIPLINES = [
    dict(id="residential", title="Residential Design", img="2024-02-residential-category.jpg", alt="Residential interior by Heidi Gubbins",
         body=["Homes designed around the personal tastes and lifestyles of those who live in them, elevated by the spatial insight of a skilled professional — and an element of unexpected enchantment.",
               "Collections are personally sourced, varied and made in small numbers. Trends never dominate; timeless appeal and individual expression do."],
         quote="It’s a journey… a creative experience where passion and professionalism are in balance."),
    dict(id="commercial", title="Commercial Projects", img="2024-02-commercial-category.jpg", alt="Commercial interior by Heidi Gubbins",
         body=["Creative concept paired with rigour on deadlines, budgets and quality — supported by stylists, carpenters, architects, landscapers, lighting specialists and technicians.",
               "Bars, restaurants, beach clubs, offices, retail and boutique hotels: larger scale, commercial realities, and the same insistence on getting it right."],
         quote="The two building blocks of a successful project are the strength of the concept and the quality of its execution in detail."),
    dict(id="refurbishment", title="Refurbishment & Renovations", img="2024-02-refur640.jpg", alt="Refurbished interior by Heidi Gubbins",
         body=["From a single room to the full refurbishment of a large property, the atelier’s technical and design teams build on a home’s architecture to make it look its very best again.",
               "A rich textural and tonal palette of natural materials creates a dialogue between spaces, forms and individual pieces."],
         quote="I am passionate about creating a mesmerising interplay between materials, textures, tones, shapes and dimensions."),
    dict(id="bespoke", title="Bespoke Furniture Design", img="2024-02-bespoke-category.jpg", alt="Bespoke furniture by Heidi Gubbins",
         body=["One-of-a-kind and limited-edition pieces, produced to measure by skilled craftsmen. Artists are sought out — and commissioned — for work that creates impact and elicits emotion.",
               "Every piece carries the DNA of the space and of those who live in it."],
         quote="There is no standard style — that is the beauty."),
]

PRODUCTS = [
    dict(slug="armor-armchair", title="Armor", kind="Armchair", img="2025-02-chair.jpg",
         body="A voluptuous, rounded silhouette of presence and poise. Its asymmetric T-like form flows into the arm, creating a dynamic visual rhythm. Fully customisable in a fabric of your choice."),
    dict(slug="minnie-pouf", title="Minnie", kind="Pouf", img="2024-06-heidi-gubbins_presented-art_2-ed.jpg",
         body="A round, heel-inspired pouf for the dressing table — whimsy and elegance in one gesture. Upholstered in velvet, leather or patterned textile to suit your space."),
    dict(slug="bubble-bench", title="Bubble", kind="Bench · David Somlo", img="2025-02-carusel9.jpg",
         body="The beauty of the imperfect. Different textures, tones, shapes and finishes give this artistic piece a unique and unrepeatable character. Artist: David Somlo."),
    dict(slug="amaya-pouf", title="Amaya", kind="Pouf Armchair", img="2025-01-carusel4.jpg",
         body="A rounded back and sculptural form of soft femininity. Equally at home in a cosy corner, at a desk or around the dining table, with an optional swivel base."),
    dict(slug="banyan-table", title="Banyan", kind="Desk & Tables", img="2025-01-carusel5.jpg",
         body="From the Banyan Collection, inspired by the grounding strength of the Banyan tree: matte white-wash, high-gloss lacquer accents and a palette of powder pink and ivory. Dining and coffee tables available to measure."),
    dict(slug="hana-no-mori", title="Hana no Mori", kind="Rug", img="2025-02-banner-down-crop.jpg",
         body="A blossom forest beneath your feet. Swirling forms and rich hues — burgundy, soft green, pastel yellow — mimic petals scattered by the wind across a landscape seen from above."),
    dict(slug="home-entertainment", title="Home Cinema", kind="Bespoke Spaces", img="2025-02-redefining-home-entertainment-20.jpg",
         body="Home cinemas reimagined as immersive experiences: textured leather-look walls, arching murals that extend the story beyond the screen, and upholstery that balances refinement with play."),
    dict(slug="home-collection", title="Home Collection", kind="Coming Soon", img="2025-01-dsc02154.jpg",
         body="Tableware, ceramics and objects designed in the studio. A first collection is in the making."),
]

PRESS = [("Essential", "June 2025", "2025-06-press-june25.jpg"), ("Essential", "April 2025", "2025-04-heidi-gubbins-press-april-25.jpg"),
         ("Design Marbella", "December 2024", "2025-02-heidi-press-1.jpg"), ("Essential", "December 2024", "2025-01-heidi-gubbins-press-dec-24-e1737997539170.jpg"),
         ("Design Marbella", "August 2023", "2023-09-portada-design-marbella.jpg"), ("Society", "April 2022", "2022-04-heidi-gubbins-press-april22.jpg"),
         ("Abode2", "March 2022", "2022-03-heidi-gubbins-press-marc22.jpg"), ("Society", "December 2021", "2021-12-dec21.jpg"),
         ("Home & Lifestyle", "Nov – Dec 2021", "2021-12-nov-dec-21-1.jpg"), ("Essential", "September 2021", "2021-10-heidi-gubbins-press-sep-21.jpg"),
         ("Society", "March 2020", "2020-04-heidi-gubbins-press-marc20.jpg"), ("Society", "February 2020", "2020-04-heidi-gubbins-press-feb-20.jpg"),
         ("Society", "January 2020", "2020-04-heidi-gubbins-press-jan20.jpg"), ("Society", "November 2019", "2020-04-heidi-gubbins-press-nov19.jpg"),
         ("Society", "October 2019", "2020-04-heidi-gubbins-press-ovct20.jpg")]

STORIES = [
    dict(slug="portrait", title="Heidi Gubbins", sub="The Artist Behind It All", cat="Portrait", img="2025-07-heidi-feartured.jpg",
         gallery=["2025-07-heidi1.jpg", "2025-07-heidi3.jpg", "2025-07-heidi5.jpg", "2025-07-heidi6.jpg", "2025-07-heidi7.jpg"],
         sections=[("The Artist Behind It All", ["Heidi Gubbins is driven by a deep love for the artistry within interior space. Her work is an intricate dance of patterns, forms and ideas, layered to resonate with each client’s sensibilities.",
                                                  "Every space, she believes, should be an individual masterpiece — telling its own story, free from imitation and filled with fresh inspiration."]),
                   ("Within the Rhythm", ["With a keen eye for detail and an intuitive feel for composition, Heidi collaborates with artists and artisans on interiors that are as bold as they are personal — a bespoke light, a custom rug, furniture made to sit within the rhythm of a room.",
                                          "She draws on the natural world, the raw beauty of materials and the skill of the craftsmen who bring her visions to life. Her spaces are more than rooms; they are experiences."])]),
    dict(slug="a-visionary-endeavour", title="A Visionary Endeavour", sub="The Tower-View Penthouse", cat="Residential Design", img="2025-07-design-stories-2-scaled.jpg",
         gallery=["2025-07-pic1.jpg", "2025-07-pic2.jpg", "2025-07-pic3.jpg", "2025-08-pic3b-scaled.jpg", "2025-07-pic4a.jpg", "2025-08-pic8b-scaled.jpg"],
         sections=[("A Tower as Compass", ["The historic stone watchtower just outside became the focal point of the entire design process — and gave the penthouse its name.",
                                            "In the open plan, lounge, kitchen, dining and TV nook were composed to feel unified while keeping distinct identities. The kitchen is the heart: a deep, dark backdrop, natural stone and smoky glass, with lighter surrounding spaces to keep the flow."]),
                   ("Layers of Visual Intrigue", ["Beneath double-height ceilings, the fireplace was conceived as an austere composition of chunky raw stone — positioned piece by piece from scaffolding to achieve perfect alignment.",
                                                  "A dining wall of raw rock meets ribbed wood panelling that conceals two hidden doors. The master bedroom is serene and sculptural, its concave wall and low bed emphasising verticality; the bathrooms are dressed in marble and stone with a quiet edge.",
                                                  "In every room, modern design is balanced with raw beauty, luxury with function — a reflection of its extraordinary surroundings."])]),
    dict(slug="ryosuke-yazaki", title="Ryosuke Yazaki", sub="Japanese Sculptor", cat="Coming Soon", img="2025-08-heidi-gubbins_design-stories_lp-banner_japanese-artist.jpg",
         gallery=[], sections=[], soon=True),
]

# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------
def arrow(): return '<span class="btn__arrow" aria-hidden="true"></span>'

def head(title, desc, R):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#f3efe8">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="icon" href="{R}assets/img/2026-05-cropped-favicon-heidi-gubbins-192x192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Hanken+Grotesk:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/main.css">
</head>
<body>
<div class="loader" aria-hidden="true">
  <div class="loader__word">{''.join(f'<span style="--i:{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate("Heidi Gubbins"))}</div>
  <div class="loader__bar"><span>Interior Design — Marbella</span><span class="loader__pct">000</span><i class="loader__line"></i></div>
</div>
<div class="progress" aria-hidden="true"></div>
<div class="curtain" aria-hidden="true"><div class="curtain__label"><span></span></div></div>
<div class="cursor" aria-hidden="true"><div class="cursor__dot"></div><div class="cursor__label">View</div></div>
<div class="grain" aria-hidden="true"></div>
<div class="lightbox" role="dialog" aria-label="Image viewer"><button class="lightbox__close">Close</button><img alt=""></div>
"""

def header(R):
    items = "".join(f'<li><a href="{R}{u}" data-label="{esc(t)}" style="--i:{i}">{esc(t)}</a></li>' for i, (t, u, _) in enumerate(NAV))
    imgs = "".join(img(R, m, t, cls="is-on" if i == 0 else "") for i, (t, _, m) in enumerate(NAV))
    soc = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL)
    return f"""<header class="header">
  <div class="wrap">
    <nav class="nav-quick nav-quick--l" aria-label="Primary">
      <a class="link-line" data-nav href="{R}studio/" data-label="The Studio">Studio</a>
      <a class="link-line" data-nav href="{R}projects/" data-label="Projects">Projects</a>
      <a class="link-line" data-nav href="{R}boutique/" data-label="Boutique">Boutique</a>
    </nav>
    <a class="brand" href="{R}" data-label="Heidi Gubbins" aria-label="Heidi Gubbins — home"><span class="brand__name">Heidi Gubbins</span><span class="brand__sub">Interior Design</span></a>
    <div class="nav-quick nav-quick--r">
      <a class="link-line hide-sm" data-nav href="{R}contact/" data-label="Contact">Enquire</a>
      <button class="menu-btn" aria-expanded="false" aria-controls="menu"><span>Menu</span><span class="menu-btn__icon"></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <div class="menu__inner">
    <ul class="menu__list">{items}</ul>
    <div class="menu__media">{imgs}</div>
    <div class="menu__foot"><span>The Golden Mile, Marbella</span><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a><span>{soc}</span></div>
  </div>
</div>"""

def footer(R):
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    nav = "".join(f'<li><a href="{R}{u}" data-label="{esc(t)}">{esc(t)}</a></li>' for t, u, _ in NAV)
    return f"""<footer class="footer dark">
  <div class="wrap">
    <a class="footer__cta" href="{R}contact/" data-label="Contact" data-cursor="Talk">
      
      <div class="footer__big mt-2"><span data-split>Let’s <em>talk.</em></span><span class="arrow-xl" aria-hidden="true"><svg width="38%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
    </a>
    <div class="grid footer__cols">
      <div class="c-1-4">
        <h4>Studio</h4>
        <p>{CONTACT['address']}</p>
        <p class="mt-1"><a class="link-line" href="{CONTACT['map']}" target="_blank" rel="noopener">View on map</a></p>
      </div>
      <div class="c-5-4">
        <h4>Enquiries</h4>
        <p>Clients &amp; Showroom<br><a href="tel:{CONTACT['tel_clients_raw']}">{CONTACT['tel_clients']}</a> · <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></p>
        <p class="mt-1">Suppliers &amp; Logistics<br><a href="tel:{CONTACT['tel_supply_raw']}">{CONTACT['tel_supply']}</a> · <a href="mailto:{CONTACT['orders']}">{CONTACT['orders']}</a></p>
      </div>
      <div class="c-9-4 grid" style="--cols:2;grid-template-columns:1fr 1fr">
        <div><h4>Index</h4><ul>{nav}</ul></div>
        <div><h4>Follow</h4><ul>{soc}</ul></div>
      </div>
      <form class="c-1-6 mt-2" data-newsletter>
        <h4>Newsletter</h4>
        <div class="field"><input type="email" name="email" id="nl-email" placeholder=" " required><label for="nl-email">Your email address</label><button class="text-link" type="submit">Subscribe {arrow()}</button></div>
        <p class="form-note" aria-live="polite"></p>
      </form>
      <div class="c-8-5 mt-2 awards" style="align-self:end;justify-content:flex-end">
        <img src="{R}assets/img/2025-05-winner-color-horizontal.png" alt="International Property Awards — Winner" style="filter:none;mix-blend-mode:normal;opacity:.85;height:58px;width:auto">
      </div>
    </div>
    <div class="footer__mark" aria-hidden="true">Gubbins</div>
    <div class="footer__base"><span>© 2026 Gubbins Interior Design S.L.</span><span>Marbella · Spain</span><a href="{R}terms/" data-label="Terms">Privacy &amp; Terms</a></div>
  </div>
</footer>"""

def page(path, title, desc, body, light_header=False):
    depth = 0 if path == "" else path.strip("/").count("/") + 1
    R = "../" * depth
    content = body(R)
    doc = (head(title, desc, R) + '<div id="app">' + header(R) +
           ('<main data-header="light">' if light_header else '<main>') + content + "</main>" + footer(R) + "</div>\n"
           '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n'
           f'<script src="{R}assets/js/app.js"></script>\n</body>\n</html>\n')
    out = SITE / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)

def phero(eyebrow, title, intro=None, aside=None):
    t = f"""<section class="phero"><div class="wrap">
  {f'<div class="phero__top"><span class="num" data-reveal>{aside}</span></div>' if aside else ''}
  <h1 class="phero__title" data-split>{title}</h1>"""
    if intro:
        t += f"""<div class="grid phero__intro"><hr class="rule c-1-4" data-line style="align-self:start;margin-top:.9em"><p class="t-lead c-6-6" data-reveal style="--d:.3s">{intro}</p></div>"""
    return t + "</div></section>"

# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------
def home(R):
    slides = [("2025-05-boho-club-spa-18.jpg", "Award — Best Luxury Spa · Boho Wellness", "projects/boho-wellness/"),
              ("2024-12-slide-bespoke-residences.jpg", "Bespoke Residences", "projects/"),
              ("2024-12-slide-interior-architecture.jpg", "Interior Architecture", "studio/"),
              ("2019-07-slide2-3.jpg", "Interior Design", "studio/"),
              ("2024-12-slide-home-living.jpg", "Home &amp; Living", "boutique/")]
    sl = "".join(f'<div class="hero__slide{" is-on" if i == 0 else ""}"><div data-speed="-.18" style="position:absolute;inset:-6% 0">{img(R, f, "", eager=i == 0)}</div></div>' for i, (f, _, _) in enumerate(slides))
    caps = "".join(f'<span>{c}</span>' for _, c, _ in slides)
    feat = [p for p in PROJECTS if p["slug"] in ("casa-vero", "tower-view-penthouse", "boho-wellness", "coral-cabana", "the-contemporary-tree-house", "bongo", "coastal-rarity")]
    cards = "".join(f"""<a class="hcard" href="{R}projects/{p['slug']}/" data-label="{esc(p['title'])}" data-cursor="View">
        <div class="media hover-zoom">{img(R, p['cover'], p['title'])}</div>
        <div class="hcard__meta"><span class="hcard__title">{esc(p['title'])}</span></div>
        <div class="t-small light-text">{esc(p['type'])} — {esc(p['loc'])}</div></a>""" for i, p in enumerate(feat))
    pillars = [("Interior Design", "studio/#residential", "2024-02-residential-category.jpg"),
               ("Interior Architecture", "studio/#refurbishment", "2024-02-refur640.jpg"),
               ("Commercial Spaces", "studio/#commercial", "2024-02-commercial-category.jpg"),
               ("Bespoke Furniture", "studio/#bespoke", "2024-02-bespoke-category.jpg"),
               ("Home &amp; Living", "boutique/", "2025-01-dsc02154.jpg")]
    pl = "".join(f"""<a class="pillar" href="{R}{u}" data-reveal style="--d:{i*.06:.2f}s"><span class="num">{i+1:02d}</span><span class="pillar__title">{t}</span><span class="pillar__thumb">{img(R, m, "")}</span></a>""" for i, (t, u, m) in enumerate(pillars))
    svc = "".join(f"<li>{esc(s)}</li>" for s in SERVICES)
    marquee = "".join(f'<span class="marquee__item">{esc(s)}</span>' for s in SERVICES[:10]) * 2
    journal = [("The Cave Room", "Boho Club Marbella", "2024-12-ashiana-project-heidi-gubbins-interior-design-marbella-8.jpg"),
               ("Design Dialogue", "Between structure and soul", "2025-01-casa-vero-heidi-gubbins-interior-design-11.jpg"),
               ("Quiet Alchemy", "Notes from the journey", "2024-03-35.jpg"),
               ("Form &amp; Flow", "Designing with curves", "2025-01-carusel1-1.jpg")]
    jr = "".join(f"""<a href="https://www.instagram.com/heidi.gubbins/" target="_blank" rel="noopener" data-cursor="Follow">
        <div class="media hover-zoom" data-img style="--d:{i*.1:.1f}s">{img(R, m, t)}</div><h4>{t}</h4><p>{s}</p></a>""" for i, (t, s, m) in enumerate(journal))
    shelf = "".join(f"""<a class="prod" href="{R}boutique/{x['slug']}/" data-label="{esc(x['title'])}" data-cursor="Discover">
        <div class="media hover-zoom" data-img style="--d:{i*.1:.1f}s">{img(R, x['img'], x['title'])}</div>
        <div class="prod__meta"><span class="prod__title">{esc(x['title'])}</span><span class="prod__kind">{esc(x['kind'])}</span></div></a>""" for i, x in enumerate(PRODUCTS[:4]))
    return f"""
<section class="hero">
  <div class="hero__slides">{sl}</div>
  <div class="hero__content"><div class="wrap">
    <h1 class="hero__title" data-split>Spaces that <em>enchant</em><br>the senses.</h1>
    <div class="hero__meta" data-reveal style="--d:.6s">
      <div class="hero__counter"><span data-hero-idx>01</span><span class="bar"><i></i></span><span>{len(slides):02d}</span></div>
      <div class="hero__caption">{caps}</div>
      <span class="scroll-hint">Scroll <i></i></span>
    </div>
  </div></div>
</section>

<section class="section"><div class="wrap">
  <div class="grid" style="row-gap:3rem">
    
    <p class="statement c-1-8" style="grid-column:1/-1" data-split>The interiors of Heidi Gubbins create an aura — a sense of <em>well-being</em> that reflects her approach yet remains an expression of your own personality.</p>
  </div>
</div></section>

<section class="hscroll dark">
  <div class="hscroll__sticky">
    <div class="hscroll__head"><h2 class="t-d1" data-split>Selected <em>work</em></h2><a class="text-link" href="{R}projects/" data-label="Projects">All projects {arrow()}</a></div>
    <div class="hscroll__track">{cards}</div>
  </div>
</section>

<section class="section"><div class="wrap grid spotlight" style="row-gap:3rem;align-items:center">
  <div class="c-1-7"><a class="media media--r43 hover-zoom" data-img href="{R}projects/boho-wellness/" data-label="Boho Wellness" data-cursor="View">{img(R, "2024-12-ashiana-project-heidi-gubbins-interior-design-marbella-main.jpg", "Boho Wellness spa, Marbella")}</a></div>
  <div class="c-9-4">
    <div class="awards" data-reveal>{img(R, "2025-05-winner-color-vert.png", "International Property Awards winner")}</div>
    
    <h2 class="t-d2 mt-2" data-split>Boho <em>Wellness</em></h2>
    <p class="t-body mt-2" data-reveal style="--d:.2s">The Cocoon, the Oyster, the Cave — a spa on the Golden Mile where every room tells its own story of nature.</p>
    <a class="text-link mt-2" href="{R}projects/boho-wellness/" data-label="Boho Wellness" data-reveal>Enter the project {arrow()}</a>
  </div>
</div></section>

<section class="band">
  <div class="band__img" data-speed="-.25">{img(R, "2024-04-paralax-home-3.jpg", "Bedroom designed by Heidi Gubbins")}</div>
  <div class="band__inner"><div class="wrap">
    
    <p class="t-d1 mt-2" data-split>Rooms that feel <em>like you.</em></p>
  </div></div>
</section>

<section class="section"><div class="wrap">
  <div class="flex-between mb-3"><h2 class="t-d2" data-split>From the <em>Boutique</em></h2><a class="text-link" href="{R}boutique/" data-label="Boutique">The full collection {arrow()}</a></div>
  <div class="shelf">{shelf}</div>
</div></section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee}</div></div>

<section class="section"><div class="wrap grid" style="row-gap:3rem;align-items:end">
  <a class="c-1-7 teaser" href="{R}design-stories/a-visionary-endeavour/" data-label="A Visionary Endeavour" data-cursor="Read">
    
    <div class="media media--r32 hover-zoom mt-2" data-img>{img(R, "2025-07-design-stories-2-scaled.jpg", "Tower-View Penthouse story")}</div>
    <h3 class="t-d3 mt-2" data-split>A Visionary <em>Endeavour</em></h3>
    <p class="t-small light-text" data-reveal>Inside the Tower-View Penthouse</p>
  </a>
  <a class="c-9-4 teaser" href="{R}press/" data-label="Press" data-cursor="Read">
    
    <div class="press-stack mt-2" data-reveal>{img(R, "2025-04-heidi-gubbins-press-april-25.jpg", "Essential, April 2025")}{img(R, "2025-06-press-june25.jpg", "Essential, June 2025")}</div>
    <h3 class="t-d3 mt-2" data-split>Essential, <em>June 2025</em></h3>
    <p class="t-small light-text" data-reveal>{len(PRESS)} editorial features since 2019</p>
  </a>
</div></section>

<section class="section paper"><div class="wrap">
  <div class="flex-between mb-3"><h2 class="t-d2" data-split>Follow Heidi’s <em>design journey</em></h2><a class="text-link" href="https://www.instagram.com/heidi.gubbins/" target="_blank" rel="noopener">@heidi.gubbins {arrow()}</a></div>
  <div class="journal">{jr}</div>
</div></section>
"""

def studio(R):
    rows = ""
    for i, d in enumerate(DISCIPLINES):
        body = "".join(f"<p>{esc(b)}</p>" for b in d["body"])
        rows += f"""<article class="grid discipline" id="{d['id']}">
  <div class="discipline__media c-1-6"><div class="media media--r45" data-img>{img(R, d['img'], d['alt'])}</div></div>
  <div class="discipline__text c-8-5">
    <span class="discipline__idx" data-reveal>0{i+1}</span>
    <h2 class="t-d2 mt-1" data-split>{esc(d['title'])}</h2>
    <div class="t-body mt-2" data-reveal style="--d:.2s">{body}</div>
    <p class="t-lead mt-2" data-reveal style="--d:.3s"><em>“{esc(d['quote'])}”</em></p>
  </div>
</article>"""
    steps = [("Listen", "Understanding lifestyle, ambitions and the character of the architecture."),
             ("Concept", "A creative narrative of materials, light, form and proportion."),
             ("Craft", "Bespoke pieces, artisans and sourcing — produced to measure."),
             ("Deliver", "Turnkey execution with rigour on deadlines, budget and quality.")]
    st = "".join(f'<div class="step" data-reveal style="--d:{i*.1:.1f}s"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
    return phero("The Studio", "An atelier of <em>sensory</em> design.",
                 "Heidi Gubbins Interior Design is an award-winning boutique atelier with a curated approach to every facet of the home — always favouring fresh ideas and inspired solutions over ‘off the shelf’.") + f"""
<section><div class="wrap"><div class="media media--r169 parallax-img" data-img><div data-speed=".1" style="height:100%">{img(R, "2024-12-the-studio-heidi-gubbins-interior-design-marbella-1.jpg", "Heidi Gubbins studio", eager=True)}</div></div>
<div class="caption"><span>The studio, Golden Mile — Marbella</span><span>Est. Marbella</span></div></div></section>

<section class="section"><div class="wrap grid" style="row-gap:3rem">
  <div class="c-1-5"><blockquote class="quote" data-reveal>I use the light, dimensions, materials and architectural details as my ingredients.<cite>Heidi Gubbins</cite></blockquote></div>
  <div class="c-7-5 t-body" data-reveal style="--d:.2s">
    <p>Working on an international scale from Marbella, the studio specialises in residential and commercial turnkey projects — beautifully styled, balanced and proportioned spaces.</p>
    <p>Each design begins with the architecture of the property and builds upon it to create a strong sense of identity: unmistakably signed, yet as unique as the project itself.</p>
  </div>
</div></section>

<section class="section--tight"><div class="wrap">
  {rows}
</div></section>

<section class="section dark"><div class="wrap">
  <div class="flex-between mb-3"><h2 class="t-d1" data-split>The <em>process</em></h2></div>
  <div class="steps mt-3">{st}</div>
</div></section>

<section class="section"><div class="wrap grid" style="row-gap:3rem">
  <div class="c-1-4"><h2 class="t-d2 mt-2" data-split>Everything, <em>considered.</em></h2></div>
  {services_list()}
</div></section>
"""

def heidi(R):
    port = ["2025-07-heidi1.jpg", "2025-07-heidi3.jpg", "2025-07-heidi5.jpg"]
    return phero("The Designer", "Heidi <em>Gubbins</em>",
                 "A professional with the soul of an artist, who approaches her work with the dedication of a craftsman.") + f"""
<section><div class="wrap grid" style="row-gap:var(--gutter)">
  <div class="c-1-7"><div class="media media--r45 parallax-img" data-img><div data-speed=".08" style="height:100%">{img(R, "2024-12-heidi-gubbins-interior-design-marbella1-1.jpg", "Heidi Gubbins in her studio", eager=True)}</div></div></div>
  <div class="c-9-4" style="align-self:end"><div class="media media--r34" data-img style="--d:.2s">{img(R, port[1], "Heidi Gubbins portrait")}</div><div class="caption"><span>Portrait, 2025</span><span>Marbella</span></div></div>
</div></section>

<section class="section"><div class="wrap grid" style="row-gap:3rem">
  
  <div class="c-5-8">
    <p class="t-d3" data-split>Aesthetics, functionality and detail — and a belief that quality always comes before quantity.</p>
    <div class="t-body mt-3" data-reveal style="--d:.2s">
      <p>Rather than spread herself thinly, Heidi dedicates herself fully to the projects she undertakes. That philosophy allows her and the team to immerse themselves completely — creating one-off spaces and, above all, environments that enchant the eye and the senses to become a source of wellbeing.</p>
    </div>
  </div>
</div></section>

<section class="section--tight"><div class="wrap stats">
  <div><div class="stat__n" data-count="18" data-suffix="+">0</div><div class="stat__l">Featured projects in Spain and abroad</div></div>
  <div><div class="stat__n" data-count="15">0</div><div class="stat__l">Editorial features in the press</div></div>
  <div><div class="stat__n" data-count="1">0</div><div class="stat__l">Award for Best Luxury Spa — Boho Wellness</div></div>
</div></section>

<section class="section dark"><div class="wrap grid" style="row-gap:3rem;align-items:center">
  <div class="c-1-5"><div class="media media--r34" data-img>{img(R, "2025-07-heidi6.jpg", "Heidi Gubbins")}</div></div>
  <div class="c-7-6">
    
    <h2 class="t-d2 mt-2" data-split>A collective, <em>constantly evolving.</em></h2>
    <div class="t-body mt-2" data-reveal style="--d:.2s"><p>Skilled professionals who love design and feel fortunate to work in it. A close-knit camaraderie lets each excel in their speciality while working together towards a single goal — your project.</p></div>
    <blockquote class="quote mt-3" data-reveal style="--d:.3s">Being flexible and open to new influences is what fuels our originality and the flow of ideas.<cite>The Studio</cite></blockquote>
  </div>
</div></section>

<section class="section"><div class="wrap grid" style="row-gap:3rem;align-items:end">
  <div class="c-1-6"><h2 class="t-d2 mt-2" data-split>Essential Magazine, <em>December 2024</em></h2>
    <div class="flex-between mt-3" style="justify-content:flex-start"><a class="btn" href="{R}press/" data-label="Press">Read in Press {arrow()}</a><a class="text-link" href="{R}design-stories/portrait/" data-label="Portrait">The portrait story {arrow()}</a></div></div>
  <div class="c-8-4"><div class="media media--r34" data-img>{img(R, "2025-03-heidi-gubbins-press-dec-24-3.jpg", "Essential magazine feature")}</div></div>
</div></section>
"""

def projects(R):
    counts = {k: sum(1 for p in PROJECTS if p["cat"] == k) for k in CATS}
    filt = f'<button class="filter is-active" data-f="all">All</button>' + "".join(f'<button class="filter" data-f="{k}">{v}</button>' for k, v in CATS.items())
    cards = "".join(f"""<a class="pcard" data-cat="{p['cat']}" href="{R}projects/{p['slug']}/" data-label="{esc(p['title'])}" data-cursor="View">
  <div class="media hover-zoom" data-img>{img(R, p['cover'], p['title'], eager=i < 2)}</div>
  <div class="pcard__meta"><span class="pcard__title">{esc(p['title'])}</span><span class="pcard__loc">{esc(p['type'])}<br>{esc(p['loc'])}</span></div></a>""" for i, p in enumerate(PROJECTS))
    rows = "".join(f"""<li data-cat="{p['cat']}"><a href="{R}projects/{p['slug']}/" data-label="{esc(p['title'])}"><span class="num">{i+1:02d}</span><span class="plist__title">{esc(p['title'])}</span><span class="plist__cat">{esc(p['type'])} — {esc(p['loc'])}</span><span class="plist__yr num">{CATS[p['cat']]}</span></a></li>""" for i, p in enumerate(PROJECTS))
    fl = "".join(img(R, p["cover"], "") for p in PROJECTS)
    return phero("Portfolio", "Projects", "A curated collection of residential and commercial interiors — completed and in the making — across Marbella and beyond.") + f"""
<section data-projects style="padding-bottom:var(--section)"><div class="wrap">
  <div class="toolbar"><div class="filters">{filt}</div></div>
  <div class="pgrid">{cards}</div>
</div></section>
"""

def project_page(p, i):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    g = [f for f in p["gallery"] if f != p["cover"]][:8]
    layout = ["g-full", "g-l", "g-r", "g-l2", "g-r2", "g-full", "g-l", "g-r"]
    ratio = {"g-full": "", "g-l": "media--r45", "g-r": "media--r34", "g-l2": "media--r34", "g-r2": "media--r45"}
    def body(R):
        figs = "".join(f"""<figure class="{layout[k]}"><div class="media {ratio[layout[k]]}" data-img data-zoom data-cursor="Zoom" style="cursor:zoom-in">{img(R, f, f"{p['title']} — image {k+1}")}</div></figure>""" for k, f in enumerate(g))
        txt = "".join(f"<p>{esc(b)}</p>" for b in p["body"])
        award = f'<span class="tag" style="color:var(--c-bone);border-color:rgba(243,239,232,.4)">{esc(p["award"])}</span>' if p.get("award") else ""
        return f"""
<section class="proj-hero">
  <div class="proj-hero__img" data-speed="-.2">{img(R, p['cover'], p['title'], eager=True)}</div>
  <div class="proj-hero__content"><div class="wrap">
    <div class="flex-between" style="align-items:center;margin-bottom:1.5rem">{award}</div>
    <h1 class="t-hero" data-split>{esc(p['title'])}</h1>
  </div></div>
</section>
<section class="section"><div class="wrap">
  <dl class="facts" data-reveal>
    <div><dt>Project</dt><dd>{esc(p['title'])}</dd></div><div><dt>Location</dt><dd>{esc(p['loc'])}</dd></div>
    <div><dt>Typology</dt><dd>{esc(p['type'])}</dd></div><div><dt>Category</dt><dd>{CATS[p['cat']]}</dd></div>
  </dl>
  <div class="grid mt-4" style="row-gap:2.5rem">
    <p class="t-d3 c-1-7" data-split>{esc(p['lead'])}</p>
    <div class="t-body c-8-5" data-reveal style="--d:.2s">{txt}</div>
  </div>
</div></section>
<section style="padding-bottom:var(--section)"><div class="wrap gallery">{figs}</div></section>
<a class="next" href="{R}projects/{nxt['slug']}/" data-label="{esc(nxt['title'])}" data-cursor="Next">
  <div class="next__img">{img(R, nxt['cover'], nxt['title'])}</div>
  <div class="next__inner"><span class="t-d1">{esc(nxt['title'])}</span><span class="btn">View project {arrow()}</span></div>
</a>
<section class="section--tight"><div class="wrap center"><a class="text-link" href="{R}projects/" data-label="Projects">Back to all projects {arrow()}</a></div></section>
"""
    page(f"projects/{p['slug']}", f"{p['title']} — {p['loc']} | Heidi Gubbins Interior Design", p["lead"], body, light_header=True)

def boutique(R):
    items = "".join(f"""<a class="prod" href="{R}boutique/{x['slug']}/" data-label="{esc(x['title'])}" data-cursor="Discover">
  <div class="media hover-zoom" data-img style="--d:{(i%3)*.12:.2f}s">{img(R, x['img'], x['title'])}</div>
  <div class="prod__meta"><span class="prod__title">{esc(x['title'])}</span><span class="prod__kind">{esc(x['kind'])}</span></div></a>""" for i, x in enumerate(PRODUCTS))
    return phero("Boutique", "Where craft meets <em>creativity.</em>",
                 "Each piece is thoughtfully created to bring timeless elegance and a personal style to your space — a reflection of Heidi’s commitment to craftsmanship and refined aesthetic.") + f"""
<section><div class="wrap"><div class="media media--r169 parallax-img" data-img><div data-speed=".1" style="height:100%">{img(R, "2025-02-heidi-gubbins-boutique-banner.jpg", "Heidi Gubbins boutique", eager=True)}</div></div></div></section>
<section class="section"><div class="wrap">
  <div class="products">{items}</div>
</div></section>
<section class="section dark"><div class="wrap center">
  
  <p class="t-d1 mt-2" data-split>Your vision, a <em>one-of-a-kind</em> masterpiece.</p>
  <a class="btn mt-3" href="{R}contact/" data-label="Contact" data-reveal>Commission a piece {arrow()}</a>
</div></section>
"""

def product_page(x, i):
    nxt = PRODUCTS[(i + 1) % len(PRODUCTS)]
    def body(R):
        return f"""
<section class="section" style="padding-top:0"><div class="wrap grid pdp">
  <div class="c-1-7"><div class="pdp__media"><div class="media" data-img>{img(R, x['img'], x['title'], eager=True)}</div></div></div>
  <div class="c-9-4">
    <a class="text-link" href="{R}boutique/" data-label="Boutique" data-reveal>← Boutique</a>
    
    <h1 class="t-d1 mt-2" data-split>{esc(x['title'])}</h1>
    <p class="t-body mt-2" data-reveal style="--d:.2s">{esc(x['body'])}</p>
    <dl class="facts mt-3" style="grid-template-columns:1fr 1fr" data-reveal><div><dt>Made</dt><dd>To measure</dd></div><div><dt>Finish</dt><dd>Customisable</dd></div></dl>
    <form class="form mt-3" data-mailto="{CONTACT['email']}">
      <input type="hidden" name="subject" value="Boutique enquiry — {esc(x['title'])}">
      <div class="field full"><input name="name" id="n" placeholder=" " required><label for="n">Name</label></div>
      <div class="field full"><input type="email" name="email" id="e" placeholder=" " required><label for="e">Email</label></div>
      <div class="field full"><textarea name="message" id="m" rows="3" placeholder=" " required></textarea><label for="m">Tell us about your space</label></div>
      <label class="check full"><input type="checkbox" name="privacy" required> I accept the privacy policy</label>
      <div class="full"><button class="btn" type="submit">Enquire {arrow()}</button><p class="form-note" aria-live="polite"></p></div>
    </form>
  </div>
</div></section>
<a class="next" href="{R}boutique/{nxt['slug']}/" data-label="{esc(nxt['title'])}" data-cursor="Next" style="height:70svh">
  <div class="next__img">{img(R, nxt['img'], nxt['title'])}</div>
  <div class="next__inner"><span class="t-d1">{esc(nxt['title'])}</span></div>
</a>"""
    page(f"boutique/{x['slug']}", f"{x['title']} {x['kind']} | Boutique — Heidi Gubbins", x["body"][:155], body)

def stories(R):
    items = ""
    for s in STORIES:
        link = f'href="{R}design-stories/{s["slug"]}/" data-label="{esc(s["title"])}" data-cursor="Read"' if not s.get("soon") else 'aria-disabled="true"'
        items += f"""<a class="story-feature" {link}>
  <div class="story-feature__media"><div class="media hover-zoom" data-img>{img(R, s['img'], s['title'])}</div></div>
  <div class="story-feature__text"><span class="tag" data-reveal>{esc(s['cat'])}</span><h2 class="t-d2 mt-2" data-split>{esc(s['title'])}</h2><p class="t-lead light-text mt-1" data-reveal><em>{esc(s['sub'])}</em></p>
  {'' if s.get('soon') else f'<span class="text-link mt-2" data-reveal>Read the story {arrow()}</span>'}</div></a>"""
    return phero("Journal", "Design <em>Stories</em>", "Step inside a world where design secrets, curated pieces and creative insights come to life — the inspiration behind Heidi’s projects.") + f"""
<section style="padding-bottom:var(--section)"><div class="wrap">{items}</div></section>"""

def story_page(s):
    if s.get("soon"): return
    def body(R):
        secs = ""
        for t, ps in s["sections"]:
            secs += f'<h2 data-split>{esc(t)}</h2>' + "".join(f"<p data-reveal>{esc(p)}</p>" for p in ps)
        g = s["gallery"]
        pics = "".join(f'<figure class="{["g-l","g-r","g-l2","g-r2","g-full","g-l"][k]}"><div class="media {["media--r45","media--r34","media--r34","media--r45","",""][k]}" data-img data-zoom data-cursor="Zoom">{img(R, f, s["title"])}</div></figure>' for k, f in enumerate(g[:6]))
        return f"""
<section class="phero" style="padding-bottom:3rem"><div class="wrap center">
  <span class="tag" data-reveal>{esc(s['cat'])}</span>
  <h1 class="t-d1 mt-2" data-split>{esc(s['title'])}</h1>
  <p class="t-lead light-text mt-2" data-reveal><em>{esc(s['sub'])}</em></p>
</div></section>
<section><div class="wrap"><div class="media media--r169 parallax-img" data-img><div data-speed=".1" style="height:100%">{img(R, s['img'], s['title'], eager=True)}</div></div></div></section>
<section class="section"><div class="wrap"><article class="article">{secs}</article></div></section>
<section style="padding-bottom:var(--section)"><div class="wrap gallery">{pics}</div></section>
<section class="section--tight"><div class="wrap center"><a class="btn" href="{R}design-stories/" data-label="Design Stories">All stories {arrow()}</a></div></section>"""
    page(f"design-stories/{s['slug']}", f"{s['title']} — {s['sub']} | Design Stories", s["sub"], body)

def press(R):
    items = "".join(f"""<div class="press__item"><div class="media" data-img data-zoom data-cursor="Zoom" style="--d:{(i%5)*.08:.2f}s;cursor:zoom-in">{img(R, f, f"{t} — {d}")}</div>
  <div class="press__pub" data-reveal>{esc(t)}</div><div class="press__date" data-reveal>{esc(d)}</div></div>""" for i, (t, d, f) in enumerate(PRESS))
    return phero("Editorial", "Press", "Features and conversations across Essential, Design Marbella, Society, Abode2 and Home &amp; Lifestyle.") + f"""
<section style="padding-bottom:var(--section)"><div class="wrap"><div class="press">{items}</div>
<div class="grid mt-4" style="border-top:1px solid var(--line);padding-top:2rem;row-gap:1rem"><p class="c-1-6 t-body">For press and marketing enquiries:</p><a class="c-7-6 t-d3 link-line" style="justify-self:end" href="mailto:{CONTACT['press']}">{CONTACT['press']}</a></div>
</div></section>"""

def contact(R):
    return phero("Contact", "Let’s create <em>together.</em>", "For any enquiry, write to us here — or visit the studio and showroom on the Golden Mile.") + f"""
<section style="padding-bottom:var(--section)"><div class="wrap grid contact-grid">
  <div class="c-1-5">
    <div class="contact-block" data-reveal><h3>Clients &amp; Showroom</h3><a href="tel:{CONTACT['tel_clients_raw']}">{CONTACT['tel_clients']}</a><p><a class="link-line" style="font-family:var(--f-sans);font-size:1.05rem" href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></p></div>
    <div class="contact-block" data-reveal style="--d:.1s"><h3>Suppliers, Warehouse &amp; Logistics</h3><a href="tel:{CONTACT['tel_supply_raw']}">{CONTACT['tel_supply']}</a><p><a class="link-line" style="font-family:var(--f-sans);font-size:1.05rem" href="mailto:{CONTACT['orders']}">{CONTACT['orders']}</a></p></div>
    <div class="contact-block" data-reveal style="--d:.2s"><h3>Press &amp; Marketing</h3><p><a class="link-line" href="mailto:{CONTACT['press']}" style="font-family:var(--f-sans);font-size:1.05rem">{CONTACT['press']}</a></p></div>
    <div class="contact-block" data-reveal style="--d:.3s"><h3>Heidi Gubbins Studio</h3><p>{CONTACT['address']}</p><p class="mt-1"><a class="text-link" style="font-family:var(--f-sans);font-size:var(--t-micro)" href="{CONTACT['map']}" target="_blank" rel="noopener">View location map {arrow()}</a></p></div>
  </div>
  <div class="c-7-6">
    <div class="media media--r32 mb-3" data-img>{img(R, "2021-09-contact-heidi-gubbins-interior-design-marbella.jpg", "Heidi Gubbins studio, Marbella", eager=True)}</div>
    <form class="form" data-mailto="{CONTACT['email']}" data-reveal>
      <div class="field"><input name="name" id="cn" placeholder=" " required autocomplete="name"><label for="cn">Name</label></div>
      <div class="field"><input name="phone" id="cp" placeholder=" " required autocomplete="tel"><label for="cp">Phone</label></div>
      <div class="field"><input type="email" name="email" id="ce" placeholder=" " required autocomplete="email"><label for="ce">Email</label></div>
      <div class="field"><input name="subject" id="cs" placeholder=" " required><label for="cs">Subject</label></div>
      <div class="field full"><textarea name="message" id="cm" rows="4" placeholder=" " required></textarea><label for="cm">Your project</label></div>
      <label class="check full"><input type="checkbox" name="privacy" required> I accept the privacy policy</label>
      <div class="full"><button class="btn" type="submit">Send enquiry {arrow()}</button><p class="form-note mt-1" aria-live="polite"></p></div>
    </form>
  </div>
</div></section>"""

def terms(R):
    return phero("Legal", "Privacy &amp; <em>Terms</em>") + f"""
<section style="padding-bottom:var(--section)"><div class="wrap"><article class="article">
<p>This website is operated by Gubbins Interior Design S.L., Marbella, Spain. We use cookies only to ensure the best experience on our website.</p>
<p>Personal data submitted through our forms is used solely to respond to your enquiry and is never shared with third parties. To exercise your rights of access, rectification or erasure, contact <a class="link-line" href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>.</p>
<p>All images and content © Gubbins Interior Design S.L. Reproduction requires prior written consent.</p>
</article></div></section>"""

if __name__ == "__main__":
    page("", "Heidi Gubbins | Luxury Interior Design — Marbella", "Award-winning boutique interior design atelier on Marbella’s Golden Mile. Residential, commercial, refurbishment and bespoke furniture.", home, light_header=True)
    page("studio", "The Studio | Heidi Gubbins Interior Design", "An award-winning boutique atelier — residential, commercial, refurbishment and bespoke furniture design.", studio)
    page("heidi-gubbins", "Heidi Gubbins | The Designer", "Interior designer with the soul of an artist and the dedication of a craftsman.", heidi)
    page("projects", "Projects | Heidi Gubbins Interior Design", "A curated portfolio of residential and commercial interiors.", projects)
    for i, p in enumerate(PROJECTS): project_page(p, i)
    page("boutique", "Boutique | Heidi Gubbins", "Bespoke furniture and objects — where craftsmanship meets creativity.", boutique)
    for i, x in enumerate(PRODUCTS): product_page(x, i)
    page("design-stories", "Design Stories | Heidi Gubbins", "Design secrets, curated pieces and creative insights.", stories)
    for s in STORIES: story_page(s)
    page("press", "Press | Heidi Gubbins", "Editorial features on Heidi Gubbins Interior Design.", press)
    page("contact", "Contact | Heidi Gubbins Interior Design", "Visit the studio on the Golden Mile, Marbella, or send us an enquiry.", contact)
    page("terms", "Privacy & Terms | Heidi Gubbins", "Privacy policy and terms.", terms)
    print("built", sum(1 for _ in SITE.rglob("index.html")), "pages")
