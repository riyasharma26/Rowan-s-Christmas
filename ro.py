# rowan_christmas_final.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, time, math

# PAGE
st.set_page_config(page_title="Rowan's Christmas Adventure", layout="centered")

# -------------------------
# CSS / THEME (high contrast)
# -------------------------
st.markdown(
    """
    <style>
    /* page background */
    html, body, [class*="css"]  {
      background: linear-gradient(180deg, #063b06 0%, #0f7a0f 50%, #7a0b0b 100%) !important;
      color: #ffffff !important;
    }
    /* big bubble title */
    .title-bubble {
      width: 94%;
      margin: 18px auto;
      padding: 30px 22px;
      border-radius: 48px;
      background: radial-gradient(circle at 25% 30%, rgba(255,255,255,0.06), rgba(0,0,0,0.04));
      border: 6px solid rgba(255,255,255,0.06);
      text-align: center;
      font-weight: 900;
      letter-spacing: 2px;
      font-size: 44px;
      color: #fffbe6;
      box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 0 6px rgba(255,255,255,0.02) inset;
    }
    /* center panel */
    .center-box {
      background: rgba(255,255,255,0.03);
      border-radius: 16px;
      padding: 18px;
      margin: 18px auto;
      text-align:center;
      max-width: 980px;
      color:#fffbe6;
    }
    /* mission buttons (bubble-letter style) */
    .mission-row { display:flex; gap:16px; justify-content:center; margin-top:20px; margin-bottom:6px; flex-wrap:wrap;}
    .mission-btn {
      background: linear-gradient(180deg,#22b14c,#15821f);
      color: #fffbe6;
      padding: 18px 22px;
      min-width: 220px;
      border-radius: 999px;
      font-weight:900;
      font-size:18px;
      border: 4px solid rgba(255,255,255,0.06);
      box-shadow: 0 8px 30px rgba(0,0,0,0.45);
    }
    .mission-btn.red {
      background: linear-gradient(180deg,#ff4b4b,#b30000);
    }
    .mission-btn.locked {
      opacity: 0.45;
      transform: scale(0.98);
      cursor: not-allowed;
      filter: grayscale(0.05);
    }
    .status-line { font-weight:800; color:#fffbe6; margin-top:8px; }
    .certificate {
      border-radius: 14px;
      padding: 18px;
      background: linear-gradient(180deg,#fffdf2,#e6ffe8);
      color:#083d08;
      max-width:920px;
      margin:18px auto;
      box-shadow: 0 12px 30px rgba(0,0,0,0.35);
      text-align:left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Header
# -------------------------
st.markdown('<div class="title-bubble">🎄 ROWAN\'S CHRISTMAS ADVENTURE 🎄</div>', unsafe_allow_html=True)
st.markdown('<div class="center-box"><h3 style="margin-bottom:6px;color:#fffbe6">Welcome Rowan — complete each mission to save Christmas!</h3><div style="opacity:0.95">Each mission shows a short animation — press Start and watch it play!</div></div>', unsafe_allow_html=True)

# -------------------------
# Session state (progress)
# -------------------------
if "m1" not in st.session_state:
    st.session_state.m1 = False
if "m2" not in st.session_state:
    st.session_state.m2 = False
if "m3" not in st.session_state:
    st.session_state.m3 = False

# -------------------------
# SVG Animation Frames (helpers)
# -------------------------
def svg_star_frame(step, w=820, h=240):
    t = step / 18.0
    size = 24 + 38 * abs(math.sin(t * math.pi))
    opacity = 0.35 + 0.65 * abs(math.cos(t * math.pi))
    svg = f"""
    <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="none" rx="12"/>
      <g transform="translate({w//2},{h//2 - 10})">
        <circle r="{size*1.9}" fill="rgba(255,240,160,{0.12+0.05*math.sin(t*3)})"/>
        <polygon points="{0,-size} {size*0.28,-size*0.28} {size*0.98,0} {size*0.28,size*0.28} {0,size} {-size*0.28,size*0.28} {-size*0.98,0} {-size*0.28,-size*0.28}"
          fill="#ffd84d" stroke="#fff1a8" stroke-width="3" style="opacity:{opacity}" />
      </g>
      <text x="50%" y="{h-18}" fill="#fffbe6" font-size="20" text-anchor="middle" font-weight="800">Lighting the Magic Star...</text>
    </svg>
    """
    return svg

def svg_car_frame(step, w=820, h=240):
    t = step / 20.0
    x = int((w-160) * (step/19.0))
    bounce = int(6 * math.sin(t*math.pi*2))
    svg = f"""
    <svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="none" rx="12"/>
      <rect x="0" y="{h-40}" width="{w}" height="40" fill="rgba(255,255,255,0.03)"/>
      <g transform="translate({x},{h-120-bounce})">
        <rect x="0" y="20" width="140" height="50" rx="14" fill="#ff4b4b" stroke="#fff" stroke-width="3"/>
        <circle cx="26" cy="78" r="16" fill="#0b0b0b"/>
        <circle cx="114" cy="78" r="16" fill="#0b0b0b"/>
        <rect x="20" y="10" width="70" height="30" rx="8" fill="#fff2f2" opacity="0.7"/>
      </g>
      <text x="50%" y="24" fill="#fffbe6" font-size="20" text-anchor="middle" font-weight="800">Rowan's Racer — zoom!</text>
    </svg>
    """
    return svg

def svg_tree_frame(step, w=820, h=240):
    t = step / 18.0
    scale = 0.7 + 0.3 * (step/18.0)
    lights = ""
    for i in range(6):
        angle = i * math.pi/6 - (t*1.8)
        lx = int((w//2) + math.cos(angle)*(30 + 22*i))
        ly = int((h//2) + math.sin(angle)*(10 + 14*i))
        op = 0.25 + 0.75 * abs(math.sin(t*2 + i))
        lights += f'<circle cx="{lx}" cy="{ly}" r="{5 + (i%2)}" fill="rgba(255,240,110,{op:.2f})" />'
    svg = f"""
    <svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="none" rx="12"/>
      <g transform="translate({w//2},{h//2 + 10}) scale({scale})">
        <polygon points="0,-86 72,18 -72,18" fill="#0b4b0b" stroke="#2ec24a" stroke-width="3"/>
        <polygon points="0,-46 55,42 -55,42" fill="#0d6610" stroke="#2ec24a" stroke-width="2"/>
        <rect x="-12" y="42" width="24" height="36" fill="#6b3a19"/>
      </g>
      {lights}
      <text x="50%" y="{h-12}" fill="#fffbe6" font-size="20" text-anchor="middle" font-weight="800">Light the Christmas Tree!</text>
    </svg>
    """
    return svg

# -------------------------
# Mission runner (defined BEFORE UI controls)
# -------------------------
def run_mission(idx):
    anim_placeholder = st.empty()
    steps = 20
    if idx == 1:
        for s in range(steps):
            svg = svg_star_frame(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.08)
        anim_placeholder.empty()
        st.success("Mission 1 complete — the Star is shining! 🌟")
        st.session_state.m1 = True
    elif idx == 2:
        for s in range(steps):
            svg = svg_car_frame(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.06)
        anim_placeholder.empty()
        st.success("Mission 2 complete — Rowan raced to help! 🚗💨")
        st.session_state.m2 = True
    elif idx == 3:
        for s in range(steps):
            svg = svg_tree_frame(s)
            anim_placeholder.markdown(svg, unsafe_allow_html=True)
            time.sleep(0.08)
        anim_placeholder.empty()
        st.success("Mission 3 complete — the Tree is lit! 🎄✨")
        st.session_state.m3 = True
    # small pause then refresh UI so buttons/ certificate update
    time.sleep(0.25)
    st.experimental_rerun()

# -------------------------
# UI: Mission Buttons (bubble-letter text; no images)
# -------------------------
st.markdown('<div class="mission-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

with col1:
    locked = False  # mission 1 always unlocked
    cls = "mission-btn" if not locked else "mission-btn locked"
    st.markdown(f'<div class="{cls}">Mission 1<br><span style="font-size:14px;opacity:0.95">Deliver the Star</span></div>', unsafe_allow_html=True)
    if not locked and st.button("Start Mission 1"):
        run_mission(1)

with col2:
    locked = not st.session_state.m1
    cls = "mission-btn red locked" if locked else "mission-btn red"
    st.markdown(f'<div class="{cls}">Mission 2<br><span style="font-size:14px;opacity:0.95">Drive the Racer</span></div>', unsafe_allow_html=True)
    if (not locked) and st.button("Start Mission 2"):
        run_mission(2)

with col3:
    locked = not st.session_state.m2
    cls = "mission-btn locked" if locked else "mission-btn"
    st.markdown(f'<div class="{cls}">Mission 3<br><span style="font-size:14px;opacity:0.95">Light the Tree</span></div>', unsafe_allow_html=True)
    if (not locked) and st.button("Start Mission 3"):
        run_mission(3)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Progress / Certificate
# -------------------------
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.06)'/>", unsafe_allow_html=True)

if st.session_state.m1 and st.session_state.m2 and st.session_state.m3:
    st.markdown('<div class="center-box"><h2 style="color:#fffbe6">All missions complete! 🎉</h2><div style="color:#fffbe6; font-weight:800">Download Rowan\'s Certificate below.</div></div>', unsafe_allow_html=True)

    # certificate creation
    def draw_rowan(size=260):
        img = Image.new("RGBA", (size, size), (255,255,255,0))
        d = ImageDraw.Draw(img)
        c = size//2
        d.ellipse((c-30, 14, c+30, 72), fill=(247,210,154), outline=(60,30,10))
        d.pieslice((c-36, 4, c+36, 68), start=180, end=360, fill=(116,75,40))
        d.line((c, 76, c, 150), fill=(10,10,10), width=6)
        d.line((c, 92, c-36, 120), fill=(10,10,10), width=6)
        d.line((c, 92, c+36, 120), fill=(10,10,10), width=6)
        d.line((c, 150, c-28, 200), fill=(10,10,10), width=6)
        d.line((c, 150, c+28, 200), fill=(10,10,10), width=6)
        return img

    def make_certificate(name="ROWAN"):
        W, H = 1200, 800
        cert = Image.new("RGB", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(cert)
        # header
        draw.rectangle([(0,0),(W,160)], fill=(180,20,20))
        try:
            tf1 = ImageFont.truetype("DejaVuSans-Bold.ttf", 56)
            tf2 = ImageFont.truetype("DejaVuSans.ttf", 32)
        except:
            tf1 = ImageFont.load_default()
            tf2 = ImageFont.load_default()
        draw.text((W//2, 36), "🎄 CHRISTMAS HERO AWARD 🎄", font=tf1, fill=(255,245,230), anchor="mm")
        avatar = draw_rowan(300)
        cert.paste(avatar, (60, 220), avatar)
        draw.text((420, 240), "This certificate is proudly awarded to", font=tf2, fill=(30,30,30))
        draw.text((420, 300), f"⭐ {name} ⭐", font=tf1, fill=(10,80,20))
        draw.text((420, 380), "For completing the Christmas Adventure — delivering the star,\nracing the sleigh, and lighting the tree!", font=tf2, fill=(40,40,40))
        draw.text((420, 520), "Santa Claus 🎅", font=tf2, fill=(130,0,0))
        draw.rectangle([(10,10),(W-10,H-10)], outline=(10,80,20), width=8)
        buf = io.BytesIO()
        cert.save(buf, format="PNG")
        buf.seek(0)
        return buf

    cert_buf = make_certificate("ROWAN")
    st.download_button("📜 Download Rowan's Certificate (PNG)", data=cert_buf, file_name="Rowan_Christmas_Certificate.png", mime="image/png")
else:
    st.markdown('<div class="center-box"><div style="font-weight:800;color:#fffbe6">Progress</div><div style="margin-top:8px;color:#fffbe6">Mission 1: ' + ('✅' if st.session_state.m1 else '❌') + '</div><div style="color:#fffbe6">Mission 2: ' + ('✅' if st.session_state.m2 else '❌') + '</div><div style="color:#fffbe6">Mission 3: ' + ('✅' if st.session_state.m3 else '❌') + '</div></div>', unsafe_allow_html=True)

st.caption("All animations are inline SVG frames — no external images. Buttons lock in order; certificate appears only when all missions are done.")
