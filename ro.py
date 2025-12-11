# rowan_christmas_reboot.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, time, math

st.set_page_config(page_title="Rowan's Christmas Adventure", layout="centered")

# -------------------------
# STYLE (red/green theme)
# -------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
      background: linear-gradient(180deg, #083d08 0%, #0b660b 40%, #7a0b0b 100%);
      color: #fff;
    }
    .title-bubble {
      width: 92%;
      margin: 16px auto;
      padding: 28px 18px;
      border-radius: 40px;
      background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.06), rgba(0,0,0,0.04));
      border: 6px solid rgba(255,255,255,0.08);
      text-align: center;
      font-weight: 900;
      letter-spacing: 2px;
      font-size: 42px;
      color: #fff7e6;
      box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 0 6px rgba(255,255,255,0.02) inset;
    }
    .mission-row {
      display:flex;
      gap:18px;
      justify-content:center;
      margin-top: 22px;
      margin-bottom: 18px;
    }
    .mission-btn {
      background: linear-gradient(180deg,#ffefef, #ffdfe0);
      color: #7a0b0b;
      padding: 16px 18px;
      min-width: 180px;
      border-radius: 999px;
      font-weight:800;
      font-size:18px;
      border: 4px solid rgba(255,255,255,0.12);
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .mission-btn.locked {
      opacity: 0.45;
      transform: scale(0.98);
      cursor: not-allowed;
    }
    .center-box {
      background: rgba(255,255,255,0.03);
      border-radius: 16px;
      padding: 18px;
      margin: 18px auto;
      text-align:center;
      max-width: 900px;
    }
    .small-note { color: #f7f7d9; opacity:0.9; }
    .done-badge { color: #d9ffd6; font-weight:900; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Page header (big bubble title)
# -------------------------
st.markdown('<div class="title-bubble">ROWAN&#8217;S CHRISTMAS ADVENTURE 🎄</div>', unsafe_allow_html=True)

st.markdown('<div class="center-box"><h3 style="margin-bottom:6px;">Welcome, Rowan! Complete the missions below to save Christmas.</h3><div class="small-note">Each mission has a short animation — press start and watch it play!</div></div>', unsafe_allow_html=True)

# -------------------------
# Session state
# -------------------------
if "m1" not in st.session_state:
    st.session_state.m1 = False
if "m2" not in st.session_state:
    st.session_state.m2 = False
if "m3" not in st.session_state:
    st.session_state.m3 = False

# helper to show mission status
def status_text(done):
    return '<span class="done-badge">✅ Done</span>' if done else '🔒 Locked' if not done else ''

# -------------------------
# Missions row (bubble-letter buttons)
# -------------------------
st.markdown('<div class="mission-row">', unsafe_allow_html=True)
cols = st.columns(3)
m_titles = ["Mission 1\nDeliver the Star", "Mission 2\nDrive the Racer", "Mission 3\nLight the Tree"]
for i, col in enumerate(cols, start=1):
    done = st.session_state[f"m{i}"]
    # only allow a mission if previous is done (except mission1)
    locked = False
    if i > 1 and not st.session_state[f"m{i-1}"]:
        locked = True
    label = f"<div style='font-weight:900'>{m_titles[i-1]}</div>"
    btn_html = f"<div class='mission-btn {'locked' if locked else ''}'>{label}</div>"
    with col:
        st.markdown(btn_html, unsafe_allow_html=True)
        key = f"start_m{i}"
        if locked:
            st.write("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='small-note'>Complete previous mission first</div>", unsafe_allow_html=True)
        else:
            if st.button(f"Start Mission {i}", key=key):
                # run that mission
                run_mission(i)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Animation functions
# -------------------------
def svg_frame_star(step, width=800, height=220):
    # blinking star grows
    t = step / 18.0
    size = 30 + 40 * abs(math.sin(t * math.pi))
    opacity = 0.4 + 0.6 * abs(math.cos(t * math.pi))
    svg = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" rx="12" fill="rgba(0,0,0,0)"/>
      <g transform="translate({width//2},{height//2})">
        <circle r="{size*1.7}" fill="rgba(255,240,160,{0.12+0.3*math.sin(t*3.1)})"/>
        <polygon points="{0,-size} {size*0.3,-size*0.3} {size,0} {size*0.3,size*0.3} {0,size} {-size*0.3,size*0.3} {-size,0} {-size*0.3,-size*0.3}"
          fill="gold" stroke="#fff4b0" stroke-width="3" style="opacity:{opacity}" />
      </g>
      <text x="50%" y="90%" fill="#fff7e6" font-size="20" text-anchor="middle" font-weight="700">Lighting the Magic Star...</text>
    </svg>"""
    return svg

def svg_frame_car(step, width=800, height=220):
    # car moves left->right and bounces
    t = step/20.0
    x = int((width-160) * (step/19.0))
    bounce = int(6 * math.sin(t*3.14*2))
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" rx="12" fill="rgba(0,0,0,0)"/>
      <rect x="0" y="{height-40}" width="{width}" height="40" fill="rgba(255,255,255,0.04)"/>
      <g transform="translate({x},{height-110-bounce})">
        <rect x="0" y="20" width="120" height="40" rx="12" fill="#ff4444" stroke="#fff" stroke-width="3"/>
        <circle cx="20" cy="66" r="14" fill="#111"/>
        <circle cx="100" cy="66" r="14" fill="#111"/>
      </g>
      <text x="50%" y="20" fill="#fff7e6" font-size="20" text-anchor="middle" font-weight="700">Rowan's Racer — zoom!</text>
    </svg>
    """
    return svg

def svg_frame_tree(step, width=800, height=220):
    # tree grows lights appear
    t = step/18.0
    scale = 0.6 + 0.4 * (step/18.0)
    lights = ""
    for i in range(6):
        angle = i * math.pi/6 - (t*2)
        lx = int((width//2) + math.cos(angle)*(30 + 20*i))
        ly = int((height//2) + math.sin(angle)*(30 + 12*i))
        # blinking
        op = 0.3 + 0.7 * abs(math.sin(t*3 + i))
        lights += f'<circle cx="{lx}" cy="{ly}" r="{6+ (i%2)}" fill="rgba(255,255,110,{op:.2f})" />'
    svg = f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" rx="12" fill="rgba(0,0,0,0)"/>
      <g transform="translate({width//2},{height//2 + 10}) scale({scale})">
        <polygon points="0,-80 60,20 -60,20" fill="#0b4b0b" stroke="#2ec24a" stroke-width="3"/>
        <polygon points="0,-40 45,40 -45,40" fill="#0d6610" stroke="#2ec24a" stroke-width="2"/>
        <rect x="-10" y="40" width="20" height="30" fill="#6b3a19"/>
      </g>
      {lights}
      <text x="50%" y="95%" fill="#fff7e6" font-size="20" text-anchor="middle" font-weight="700">Light the Christmas Tree!</text>
    </svg>
    """
    return svg

# -------------------------
# Mission runner (animates and marks done)
# -------------------------
def run_mission(idx):
    anim_placeholder = st.empty()
    steps = 20
    if idx == 1:
        for s in range(steps):
            svg = svg_frame_star(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.08)
        anim_placeholder.empty()
        st.success("Mission 1 complete — the Star is shining! 🌟")
        st.session_state.m1 = True
    elif idx == 2:
        for s in range(steps):
            svg = svg_frame_car(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.06)
        anim_placeholder.empty()
        st.success("Mission 2 complete — Rowan raced to help! 🚗💨")
        st.session_state.m2 = True
    elif idx == 3:
        for s in range(steps):
            svg = svg_frame_tree(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.08)
        anim_placeholder.empty()
        st.success("Mission 3 complete — the Tree is lit! 🎄✨")
        st.session_state.m3 = True
    # small pause then refresh UI to show certificate availability
    time.sleep(0.3)
    st.experimental_rerun()

# -------------------------
# Certificate (only when all done)
# -------------------------
if st.session_state.m1 and st.session_state.m2 and st.session_state.m3:
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1)'/>", unsafe_allow_html=True)
    st.markdown('<div class="center-box"><h2 style="margin-bottom:8px;">All missions complete! Download Rowan\'s Certificate 🎉</h2></div>', unsafe_allow_html=True)

    def draw_rowan_stick(size=220):
        img = Image.new("RGBA", (size, size), (255,255,255,0))
        d = ImageDraw.Draw(img)
        center = size//2
        # head
        d.ellipse((center-28, 20, center+28, 76), fill=(247,210,154), outline=(60,30,10))
        # hair
        d.pieslice((center-34, 6, center+34, 64), start=180, end=360, fill=(116,75,40))
        # body
        d.line((center, 76, center, 140), fill=(10,10,10), width=6)
        # arms
        d.line((center, 92, center-36, 120), fill=(10,10,10), width=6)
        d.line((center, 92, center+36, 120), fill=(10,10,10), width=6)
        # legs
        d.line((center, 140, center-28, 190), fill=(10,10,10), width=6)
        d.line((center, 140, center+28, 190), fill=(10,10,10), width=6)
        return img

    def make_certificate_image(name="ROWAN"):
        W, H = 1200, 800
        cert = Image.new("RGB", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(cert)
        # header
        draw.rectangle([(0,0),(W,160)], fill=(180,20,20))
        try:
            tf1 = ImageFont.truetype("DejaVuSans-Bold.ttf", 56)
            tf2 = ImageFont.truetype("DejaVuSans.ttf", 36)
        except:
            tf1 = ImageFont.load_default()
            tf2 = ImageFont.load_default()
        draw.text((W//2, 36), "🎄 CHRISTMAS HERO AWARD 🎄", font=tf1, fill=(255,245,230), anchor="mm")
        # place stick Rowan
        avatar = draw_rowan_stick(300)
        cert.paste(avatar, (60, 220), avatar)
        # text
        draw.text((400, 240), f"This certificate is proudly awarded to", font=tf2, fill=(30,30,30))
        draw.text((400, 300), f"⭐ {name} ⭐", font=tf1, fill=(10,80,20))
        draw.text((400, 380), "For completing the Christmas Adventure\n— delivering the star, racing the sleigh, and lighting the tree!", font=tf2, fill=(40,40,40))
        draw.text((400, 520), "Santa Claus 🎅", font=tf2, fill=(130,0,0))
        # border
        draw.rectangle([(10,10),(W-10,H-10)], outline=(10,80,20), width=8)
        buf = io.BytesIO()
        cert.save(buf, format="PNG")
        buf.seek(0)
        return buf

    cert_buf = make_certificate_image("ROWAN")
    st.download_button("📜 Download Rowan's Certificate (PNG)", data=cert_buf, file_name="Rowan_Christmas_Certificate.png", mime="image/png")

else:
    # show progress
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.06)'/>", unsafe_allow_html=True)
    st.markdown('<div class="center-box"><h4>Progress</h4></div>', unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-weight:800; color:#fff7e6'>Mission 1: {'✅' if st.session_state.m1 else '❌'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-weight:800; color:#fff7e6'>Mission 2: {'✅' if st.session_state.m2 else '❌'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-weight:800; color:#fff7e6'>Mission 3: {'✅' if st.session_state.m3 else '❌'}</div>", unsafe_allow_html=True)

st.caption("This version uses only shapes & SVG/CSS generated in-app — no external images or file paths required.")
