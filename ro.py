# rowan_map_game.py
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io, time

st.set_page_config(page_title="Rowan's Map Adventure", layout="wide")

# ---------- Config: point these to your uploaded files ----------
MAP_PATH = "/mnt/data/ro_map.avif"            # your uploaded map (preferred)
GARAGE_PATH = "/mnt/data/ro_garage.jpg"      # garage scene (uploaded)
AVATAR_PATH = "/mnt/data/A_2D_digital_illustration_of_a_young_boy_depicts_h.png"  # avatar file

# Fallback placeholder images (online)
FALLBACK_MAP = "https://i.imgur.com/0Z9QKsD.png"
FALLBACK_GARAGE = "https://i.imgur.com/Br6sz5Q.png"
FALLBACK_AVATAR = "https://i.imgur.com/auZfjBw.png"

# Sounds (optional)
SND_BELL = "https://www.myinstants.com/media/sounds/christmas-bells.mp3"
SND_ENGINE = "https://www.myinstants.com/media/sounds/car-starting.mp3"
SND_MAGIC = "https://www.myinstants.com/media/sounds/magic-wand-1.mp3"

# ---------- Path bubbles definition ----------
# Each bubble: (id, label, percent_x, percent_y, icon_emoji)
# percent positions are relative to map width/height (0-100)
BUBBLES = [
    (1, "Garage", 8, 78, "🚗"),
    (2, "Candy Forest", 30, 62, "🍬"),
    (3, "Donkey Hill", 50, 44, "🐵"),
    (4, "Sleigh Fix", 68, 30, "⚙️"),
    (5, "Rooftop", 88, 18, "🎁"),
]

# ---------- Utils ----------
def local_url(path):
    p = Path(path)
    if p.exists():
        return f"file://{p.resolve()}"
    return None

def read_query_int(key, default=None):
    qp = st.experimental_get_query_params()
    if key in qp and len(qp[key]) > 0:
        try:
            return int(qp[key][0])
        except:
            return default
    return default

def set_query_param(**kwargs):
    st.experimental_set_query_params(**{k:str(v) for k,v in kwargs.items()})

# certificate generator
def make_certificate(avatar_path, name="ROWAN"):
    W, H = 1200, 800
    cert = Image.new("RGBA", (W, H), (255,255,255,255))
    d = ImageDraw.Draw(cert)
    # fonts
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # header
    d.rectangle([(0,0),(W,160)], fill=(200,30,80))
    d.text((40,40), "🎄 CHRISTMAS HERO AWARD 🎄", fill="white", font=title_font)

    # avatar
    try:
        av = Image.open(avatar_path).convert("RGBA")
        av = av.resize((320,320), Image.LANCZOS)
        cert.paste(av, (60,200), av)
    except Exception as e:
        d.rectangle([(60,200),(380,520)], outline="black")
        d.text((80,320), "Avatar\nmissing", fill="black", font=body_font)

    # text
    d.text((420,220), f"This certificate is proudly awarded to:", fill=(30,30,30), font=body_font)
    d.text((420,300), f"⭐ {name} ⭐", fill=(10,70,180), font=title_font)
    d.text((420,420), "For bravely helping Santa,\nrescuing the reindeer,\nfixing the sleigh,\nand saving Christmas!", fill=(30,30,30), font=body_font)
    d.text((420,620), "Santa Claus 🎅", fill=(80,0,0), font=body_font)

    buf = io.BytesIO()
    cert.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ---------- Session state ----------
if "completed" not in st.session_state:
    # completed bubbles list (start with bubble 1 unlocked)
    st.session_state.completed = {1: True}
    st.session_state.current_mission = None

# ---------- Map rendering (HTML) ----------
# map sources (prefer local uploaded files)
map_src = local_url(MAP_PATH) or FALLBACK_MAP
avatar_src = local_url(AVATAR_PATH) or FALLBACK_AVATAR

# read mission param (if user clicked a bubble link like ?mission=2)
selected = read_query_int("mission", default=None)
if selected:
    st.session_state.current_mission = selected

# Build the HTML for map with clickable bubbles that link to ?mission=N
# and a moving avatar that animates to the selected bubble using JS.
bubble_html_parts = []
for bid, label, px, py, emoji in BUBBLES:
    locked = not st.session_state.completed.get(bid, False)
    # If a bubble is locked, add a lock overlay and make it non-clickable
    if locked:
        # still render but link to same map (no mission)
        anchor = "#"
        bubble_class = "bubble locked"
    else:
        anchor = f"?mission={bid}"
        bubble_class = "bubble unlocked"

    # each bubble is positioned with left/top percentages
    bubble_html_parts.append(
        f"""<a href="{anchor}" class="{bubble_class}" data-bid="{bid}" title="{label}">
                <div class="emoji">{emoji}</div>
                <div class="lbl">{label}</div>
            </a>"""
    )

# JS mapping of positions for avatar to animate to
positions_js_array = ",\n".join([f"{{id:{bid}, x:{px}, y:{py}}}" for bid,_,px,py,_ in BUBBLES])

html = f"""
<div style="position:relative; width:100%; max-width:1000px; margin:0 auto;">
  <div id="map" style="position:relative; background-image:url('{map_src}'); background-size:cover; width:100%; padding-top:56.25%; border-radius:16px; box-shadow:0 8px 30px rgba(0,0,0,0.25); overflow:hidden;">
    <!-- bubbles -->
    <style>
      .bubble {{
        position:absolute;
        transform:translate(-50%,-50%);
        display:flex;
        flex-direction:column;
        align-items:center;
        text-decoration:none;
        transition: transform .25s ease, box-shadow .2s;
        cursor:pointer;
      }}
      .bubble .emoji {{
        width:64px; height:64px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:32px; background:linear-gradient(180deg,#fff,#ffd6e0);
        box-shadow: 0 6px 16px rgba(0,0,0,0.18);
        border: 4px solid rgba(255,255,255,0.6);
      }}
      .bubble .lbl {{
        margin-top:8px; font-weight:600; color:#ffffff; text-shadow:0 2px 6px rgba(0,0,0,0.6);
        font-size:14px;
      }}
      .bubble.unlocked:hover {{ transform:translate(-50%,-60%) scale(1.06); }}
      .bubble.locked {{ opacity:0.45; filter:grayscale(0.15); cursor:default; }}
      .bubble.locked .emoji::after {{
        content: '🔒'; position:absolute; right:-6px; top:-6px; transform:scale(.9);
      }}

      /* avatar */
      .avatar {{
        position:absolute; width:120px; height:120px; transform:translate(-50%,-50%);
        transition: left 1s cubic-bezier(.2,.9,.2,1), top 1s cubic-bezier(.2,.9,.2,1), transform .6s;
        will-change:left,top;
        pointer-events:none;
      }}
      .sparkle {{
        position:absolute; width:40px; height:40px; border-radius:50%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.95), rgba(255,255,255,0) 40%);
        filter:blur(4px); opacity:0.9;
        transform:translate(-50%,-50%) scale(.6);
        animation: pop 1.1s ease-out infinite;
      }}
      @keyframes pop {{
        0% {{ transform:translate(-50%,-50%) scale(.6); opacity:0.0; }}
        50% {{ transform:translate(-50%,-50%) scale(1.1); opacity:1.0; }}
        100% {{ transform:translate(-50%,-50%) scale(.6); opacity:0.0; }}
      }}
    </style>

    <!-- inject bubbles with inline positions -->
    <div id="bubbles_container">
    """

# Now append bubble elements with inline styles for positions
for (bid, label, px, py, emoji) in BUBBLES:
    locked = not st.session_state.completed.get(bid, False)
    anchor = "#" if locked else f"?mission={bid}"
    cls = "locked" if locked else "unlocked"
    html += f"""
    <a href="{anchor}" class="bubble {cls}" style="left:{px}%; top:{py}%;" data-bid="{bid}">
      <div class="emoji">{emoji}</div>
      <div class="lbl">{label}</div>
    </a>
    """

# avatar element - initial position: bubble 1
initial_bubble = 1
for b in BUBBLES:
    if b[0] == initial_bubble:
        initx, inity = b[2], b[3]
        break

html += f"""
    </div>

    <img id="avatar" class="avatar" src="{avatar_src}" style="left:{initx}%; top:{inity}%;"/>
  </div>
</div>

<script>
  const positions = [{positions_js_array}];
  // find selected mission from query param
  function getParam(name) {{
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
  }}
  const sel = getParam('mission');
  if (sel) {{
    const id = parseInt(sel);
    const p = positions.find(x => x.id===id);
    if (p) {{
      // move avatar
      const avatar = document.getElementById('avatar');
      // tiny delay to ensure CSS and layout computed
      setTimeout(()=> {{
        avatar.style.left = p.x + '%';
        avatar.style.top = p.y + '%';
        // small scale animation
        avatar.style.transform = 'translate(-50%,-50%) scale(1.03)';
        setTimeout(()=> avatar.style.transform = 'translate(-50%,-50%) scale(1)', 800);
      }}, 120);
    }}
  }}
</script>
"""

# Render the interactive map component
components.html(html, height=600, scrolling=True)

# ---------- Right pane: mission details and logic ----------
st.markdown("## Rowan's Christmas Path")
col1, col2 = st.columns([3,1])

with col1:
    st.write("Click any unlocked bubble on the map to go to that mission.")
    # Show mission panel based on selected mission in query params
    mission = st.session_state.current_mission
    if mission is None:
        st.info("No mission selected. Start by clicking the first bubble (Garage).")
    else:
        st.markdown(f"### Mission {mission}: {dict((b[0],b[1]) for b in BUBBLES)[mission]}")
        # Simple mission screens
        if mission == 1:
            # garage mission
            img_src = local_url(GARAGE_PATH) or FALLBACK_GARAGE
            st.image(img_src, use_column_width=True)
            st.write("Rowan jumps into the Red Racer to search for the missing reindeer.")
            if st.button("Complete Garage mission (find the racer)"):
                st.session_state.completed[1] = True
                # unlock bubble 2
                st.session_state.completed[2] = True
                st.success("Garage mission complete! Candy Forest unlocked.")
                # Clear query param so clicking will retrigger animation next time
                set_query_param()
                time.sleep(.2)
                st.experimental_rerun()

        elif mission == 2:
            st.image(local_url(MAP_PATH) or FALLBACK_MAP, use_column_width=True)
            st.write("Candy Cane Forest — choose to walk with Donkey Kong or race.")
            c1, c2 = st.columns(2)
            if c1.button("Walk with Donkey Kong (complete)"):
                st.session_state.completed[2] = True
                st.session_state.completed[3] = True
                st.success("Donkey Hill unlocked!")
                set_query_param()
                st.experimental_rerun()
            if c2.button("Drive (fast) — complete"):
                st.session_state.completed[2] = True
                st.session_state.completed[3] = True
                st.success("Donkey Hill unlocked!")
                set_query_param()
                st.experimental_rerun()

        elif mission == 3:
            st.image(local_url(MAP_PATH) or FALLBACK_MAP, use_column_width=True)
            st.write("Donkey Hill — Rowan teams with DK and finds a clue for the sleigh.")
            if st.button("Complete Donkey Hill"):
                st.session_state.completed[3] = True
                st.session_state.completed[4] = True
                st.success("Sleigh Fix unlocked!")
                set_query_param()
                st.experimental_rerun()

        elif mission == 4:
            st.image(local_url(MAP_PATH) or FALLBACK_MAP, use_column_width=True)
            st.write("Sleigh Fix — pick a tool to fix Santa’s sleigh.")
            c1, c2, c3 = st.columns(3)
            if c1.button("Star Hammer"):
                st.session_state.completed[4] = True
                st.session_state.completed[5] = True
                st.success("Rooftop unlocked!")
                set_query_param()
                st.experimental_rerun()
            if c2.button("Light Blade"):
                st.session_state.completed[4] = True
                st.session_state.completed[5] = True
                st.success("Rooftop unlocked!")
                set_query_param()
                st.experimental_rerun()
            if c3.button("Spark Wand"):
                st.session_state.completed[4] = True
                st.session_state.completed[5] = True
                st.success("Rooftop unlocked!")
                set_query_param()
                st.experimental_rerun()

        elif mission == 5:
            st.image(local_url(MAP_PATH) or FALLBACK_MAP, use_column_width=True)
            st.write("Rooftop — deliver the present!")
            if st.button("Deliver Present — Finish Adventure"):
                st.session_state.completed[5] = True
                st.success("You saved Christmas 🎉")
                # create certificate and offer download
                buf = make_certificate(AVATAR_PATH if Path(AVATAR_PATH).exists() else FALLBACK_AVATAR, name="ROWAN")
                st.download_button("Download Rowan's Certificate (PNG)", data=buf, file_name="Rowan_Certificate.png", mime="image/png")
                set_query_param()
                st.experimental_rerun()

with col2:
    st.write("Progress")
    # show bubble list with lock/unlock
    for bid, label, px, py, emoji in BUBBLES:
        unlocked = st.session_state.completed.get(bid, False)
        st.markdown(f"- {emoji} **{label}** — {'✅' if unlocked else '🔒'}")

st.markdown("---")
st.caption("If the map image doesn't render, replace MAP_PATH and GARAGE_PATH constants at the top with your local file paths or with image URLs. The app uses file:// paths when local files exist.")
