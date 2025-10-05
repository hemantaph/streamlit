"""
Streamlit Portfolio — single-page layout matching the provided Notion look

Folder structure (expected):

assets/
  cover.png                # 1) cover picture
  profile.jpg              # 2) profile picture (square or circle crop)
  divider.png              # 3, 8, 13) small rectangular picture used as a divider strip
  gallery/
    about.jpg              # card thumbnails (optional)
    projects.jpg
    blogs.jpg
    social.jpg
  extras/                  # 11) photography & artworks (any *.jpg/png here will be shown)
    img_01.jpg
    img_02.jpg

Run locally:
  pip install -r requirements.txt
  streamlit run app.py

requirements.txt
-----------------
streamlit>=1.36
Pillow
-----------------
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Tuple

import streamlit as st
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Hemanta Ph. — Portfolio",
    page_icon="🪐",
    layout="wide",
)

# ---------- PATHS ----------
ASSETS = Path(".assets")
COVER = ASSETS / "cover.png"
PROFILE = ASSETS / "profile.png"
DIVIDER = ASSETS / "divider1.png"  # small rectangular strip
GALLERY_DIR = ASSETS / "gallery"
EXTRAS_DIR = ASSETS / "extras"

# ---------- FIXED NAVBAR (move to very top) ----------
st.markdown(
        """
        <style>
            .hamburger-navbar {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 42px;
                background: #e6f2ff;
                color: #222;
                z-index: 10001;
                display: flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.07);
                padding: 0 18px;
                justify-content: space-between;
            }
            .hamburger-navbar .nav-title {
                font-size: 1.05rem;
                font-weight: 700;
                letter-spacing: 1px;
                color: #222;
            }
            .hamburger-navbar .nav-links {
                display: flex;
                gap: 12px;
            }
            .hamburger-navbar .nav-link {
                color: #222;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.98rem;
                padding: 6px 12px;
                border-radius: 6px;
                transition: background 0.2s;
                display: block;
            }
            .hamburger-navbar .nav-link:hover {
                background: #cbe6ff;
            }
            /* Pure CSS Hamburger Toggle */
            #menu-toggle {
                display: none;
            }
            .hamburger-navbar .hamburger {
                display: none;
                flex-direction: column;
                cursor: pointer;
                margin-left: 18px;
            }
            .hamburger-navbar .hamburger span {
                height: 3px;
                width: 22px;
                background: #222;
                margin: 3px 0;
                border-radius: 2px;
                transition: 0.3s;
            }
            @media (max-width: 700px) {
                .hamburger-navbar {
                    height: 44px;
                    padding: 0 8px;
                }
                .hamburger-navbar .nav-links {
                    display: none;
                    position: absolute;
                    top: 44px;
                    left: 0;
                    width: 100vw;
                    background: #e6f2ff;
                    flex-direction: column;
                    gap: 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
                }
                .hamburger-navbar .nav-link {
                    padding: 14px 18px;
                    border-radius: 0;
                    border-bottom: 1px solid #cbe6ff;
                }
                #menu-toggle:checked + .hamburger + .nav-links {
                    display: flex;
                }
                .hamburger-navbar .hamburger {
                    display: flex;
                }
            }
            .main, .block-container, .wrap {
                margin-top: -70px !important;
            }
                    .main, .block-container {
                        max-width: 960px;
                        margin-left: auto;
                        margin-right: auto;
                        padding-left: 10px;
                        padding-right: 10px;
                    }
                    .wrap {
                        max-width: 960px;
                        margin: 0 auto;
                        padding-left: 10px;
                        padding-right: 10px;
                    }
            .hero-name {font-size: 3rem; font-weight: 800; margin: .25rem 0 0 0}
            .light-sub {opacity:.7; margin-top: .25rem}
            .blue-subheader {background:#e6f2ff; padding:10px 14px; border-radius:8px; font-weight:700;}
            .blockquote {border-left: 4px solid #999; padding: 10px 14px; background: #fafafa; border-radius: 6px;}
            .link-bubble {display:inline-block; padding:10px 16px; border-radius:8px; border:1px solid rgba(0,0,0,.15); background:white; margin-right:10px; text-decoration:none;}
            .card {border:1px solid rgba(0,0,0,.08); border-radius:14px; padding:12px;}
            .card img {border-radius:10px;}
            .card h4 {margin:.5rem 0 .25rem 0}
            .muted {color:rgba(0,0,0,.55)}
            .footer {text-align:center; opacity:.7; margin: 24px 0 8px 0}
            header[data-testid="stHeader"] { display: none; }
        </style>
        <div class='hamburger-navbar'>
            <span class='nav-title'>Hemanta Ph. Portfolio</span>
            <input type='checkbox' id='menu-toggle' style='display:none;'>
            <label class='hamburger' for='menu-toggle'>
                <span></span>
                <span></span>
                <span></span>
            </label>
            <div class='nav-links'>
                <a class='nav-link' href="#about">About</a>
                <a class='nav-link' href="#projects">Projects</a>
                <a class='nav-link' href="#blogs">Blogs</a>
                <a class='nav-link' href="#extras">Extras</a>
                <a class='nav-link' href="#contact">Contact</a>
            </div>
        </div>
        <div class='wrap'>
        """,
        unsafe_allow_html=True,
)



# ---------- 1) COVER: Three.js Diagram with Profile Overlay ----------
import streamlit.components.v1 as components
from base64 import b64encode

# Prepare profile image as base64 for overlay
if PROFILE.exists():
    with open(PROFILE, "rb") as pf:
        pdata = pf.read()
        pb64 = b64encode(pdata).decode()
        profile_html = f"<img src='data:image/png;base64,{pb64}' style='width:80px;height:80px;object-fit:cover;border-radius:50%;margin-right:18px;border:2px solid #fff;'>"
else:
    profile_html = "<div style='color:#fff;opacity:.7;'>Add .assets/profile.png</div>"


# Inject profile image src into overlay in gwlensing.html
with open(".assets/gwlensing.html", "r") as f:
    html_content = f.read()
if PROFILE.exists():
    profile_src = f"data:image/png;base64,{pb64}"
else:
    profile_src = ""
html_content = html_content.replace("PROFILE_SRC", profile_src)

# Inject robust CSS to ensure the iframe and its immediate containers show rounded corners.
# We target multiple possible Streamlit container selectors and the iframe itself with
# !important so rounding is visible even when Streamlit wraps the component.
st.markdown(
        """
        <style>
            /* Very high-specificity rules to target Streamlit's component iframe */
            .stApp iframe, .stApp main iframe, div[data-testid="stComponent"] iframe, iframe[srcdoc] {
                border-radius: 10px !important;
                overflow: hidden !important;
                border: none !important;
                box-shadow: 0 2px 16px rgba(0,0,0,0.10) !important;
            }
            /* Also ensure the immediate parent container clips overflow */
            div[data-testid="stVerticalBlock"] { overflow: visible; }
            div[data-testid="stComponent"] { border-radius: 10px !important; overflow: hidden !important; }
        </style>
        """,
        unsafe_allow_html=True,
)

# Render the original HTML content directly into the component iframe (avoid wrapping a full
# HTML document inside another wrapper — that can interfere with clipping and rendering).
# Render the HTML inside an iframe we control so we can guarantee rounded corners.
from base64 import b64encode as _b64
html_b64 = _b64(html_content.encode()).decode()
iframe_html = f"""
<div style='width:100%; max-width:1000px; margin:0 auto; height:420px; overflow:hidden; border-radius:10px; box-shadow:0 2px 16px rgba(0,0,0,0.10);'>
    <iframe
        src='data:text/html;base64,{html_b64}'
        style='width:100%; height:600px; border:0; margin-top: -150px;'
        sandbox='allow-scripts allow-same-origin'
    ></iframe>
</div>
"""
st.markdown(iframe_html, unsafe_allow_html=True)

# Add some vertical space between the iframe and divider
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ---------- 2) PROFILE (left) + NAME (right) ----------
# (Profile and name now appear in the cover overlay above)

# ---------- 3) SMALL RECTANGULAR DIVIDER ----------
if DIVIDER.exists():
    st.image(str(DIVIDER))

# ---------- 4) SUBHEADER: Welcome ----------
st.markdown("<div class='blue-subheader'>Welcome to my portfolio</div>", unsafe_allow_html=True)

# ---------- 5) QUOTE STYLE INTRO ----------
INTRO = (
    "I am an astro-physicist with a curious mind, hoping to explore the universe through quantum physics and general relativity. "
    "Besides, my interest lies in the application my coding and programming prowess in statistics and data analysis of scientific problems. "
    "Lastly, I am also a writer who aims for a unique amalgamation of science, literature, history and arts. Knowledge is what I seek, "
    "and art is how I find its elegance and beauty."
)
st.markdown(f"<div class='blockquote'>{INTRO}</div>", unsafe_allow_html=True)

# ---------- 6) RECTANGULAR LINK BUBBLES ----------
LINKS = [
    ("Resume", "#", "📄"),
    ("University Website", "#", "🏛️"),
    ("GitHub", "https://github.com/hemantaph", "🐙"),
]
link_html = "".join([f"<a class='link-bubble' href='{url}' target='_blank'>{icon} {txt}</a>" for txt, url, icon in LINKS])
st.markdown(link_html, unsafe_allow_html=True)

st.divider()

# ---------- 7) CONTENT GALLERY (grids): About Me, Projects, Blogs, Social ----------
card_items: List[Tuple[str,str,str]] = [
    ("About Me", str((GALLERY_DIR / "about.jpg")), "Education · Research · Activities"),
    ("Projects", str((GALLERY_DIR / "projects.jpg")), "gwsnr · Waveforms · Tools"),
    ("Blogs", str((GALLERY_DIR / "blogs.jpg")), "Thoughts · Physics · Travel"),
    ("Social", str((GALLERY_DIR / "social.jpg")), "Links and handles"),
]

c1, c2 = st.columns(2)
for i, (title, img_path, caption) in enumerate(card_items):
    with (c1 if i % 2 == 0 else c2):
        with st.container(border=False):
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if Path(img_path).exists():
                st.image(img_path)
            st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
            st.caption(caption)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------- 8) SMALL RECTANGULAR DIVIDER ----------
if DIVIDER.exists():
    st.image(str(DIVIDER))

# ---------- 9) SUBHEADER: Extras ----------
st.markdown("<div class='blue-subheader'>Extras</div>", unsafe_allow_html=True)

# ---------- 10) QUOTE STYLE: Extras intro ----------
EXTRA_QUOTE = (
    "Besides my dedication to physics, I also induldge myself to certain hobbies. It keeps me hang on to a artistic lookout of life. "
    "Enjoy the photos and art works shown below."
)
st.markdown(f"<div class='blockquote'>{EXTRA_QUOTE}</div>", unsafe_allow_html=True)

# ---------- 11) GALLERY for photography & artworks (auto-load images) ----------
def load_images_from(folder: Path, exts=(".jpg", ".jpeg", ".png")) -> List[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in exts])

imgs = load_images_from(EXTRAS_DIR)
if not imgs:
    st.info("Put images in assets/extras/ to populate this gallery.")
else:
    # 3-column grid
    ncols = 3
    rows = [imgs[i:i+ncols] for i in range(0, len(imgs), ncols)]
    for row in rows:
        cols = st.columns(ncols)
        for col, imgp in zip(cols, row):
            with col:
                st.image(str(imgp))

# ---------- 12) FOOTER: Contact ----------
st.markdown("<div class='footer'>|  <b>Contact</b>  |  <a href='mailto:your.email@example.com'>email</a>  |</div>", unsafe_allow_html=True)

# ---------- 13) SMALL RECTANGULAR DIVIDER (footer) ----------
if DIVIDER.exists():
    st.image(str(DIVIDER))

# close wrapper
st.markdown("</div>", unsafe_allow_html=True)
