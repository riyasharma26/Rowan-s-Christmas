# rowan_christmas_game.py
import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import time
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Rowan's Christmas Adventure — Animated", layout="wide")

# ---------- CONFIG ----------
AVATAR_PATH = "/mnt/data/A_2D_digital_illustration_of_a_young_boy_depicts_h.png"
# If running locally and your avatar is somewhere else, update that path.

# Background images (you can replace these with your own URLs or local files)
BG_GARAGE = "https://i.imgur.com/Br6sz5Q.png"
BG_FOREST = "https://i.imgur.com/0Z9QKsD.png"
BG_ROOFTOP = "https://i.imgur.com/k6k4QNk.png"

# Simple action sounds (external urls). If you run offline remove or replace.
SND_BELL = "https://www.myinstants.com/media/sounds/christmas-bells.mp3"
SND_ENGINE = "https://www.myinstants.com/media/sounds/car-starting.mp3"
SND_MAGIC = "https://www.myinstants.com/media/sounds/magic-wand-1.mp3"

# ---------- SESSION STATE ----------
if "scene" not in st.session_state:
    st.session_state.scene = "intro"
if "action" not in st.session_state:
    st.session_state.action = None
if "last_move" not in st.session_state:
    st.session_state.last_move = 0  # timestamp for retriggering animation

def go(scene, action=None):
    st.session_state.scene = scene
    st.session_state.action = action
    st.session_state.last_move = time.time()

# ---------- Helper: play sound ----------
def play_sound_html(src, loop=False):
    loop_attr = "loop" if loop else ""
    html = f"""<audio autoplay {loop_attr}><source src="{src}" type="audio/mp3"></audio>"""
    st.components.v1.html(html, height=10)

# ---------- Helper: generate certificate PNG ----------
def make_certificate(avatar_path, name="ROWAN"):
    # Create a simple certificate image programmatically
    W, H = 1200, 800
    cert = Image.new("RGB", (W, H), (255, 250, 240))
    draw = ImageDraw.Draw(cert)

    # Draw header
    draw.rectangle([(0,0),(W,150)], fill=(230,20,80))
    header_font = ImageFont.load_default()
    try:
        header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    draw.text((40, 45), "🎄 CHRISTMAS HERO AWARD 🎄", fill="white", font=title_font)

    # Insert avatar (left)
    try:
        avatar = Image.open(avatar_path).convert("RGBA")
        avatar = avatar.resize((320, 320), Image.LANCZOS)
        cert.paste(avatar, (60, 200), avatar)
    except Exception as e:
        draw.rectangle([(60,200),(380,520)], outline="black")
        draw.text((80,320), "Avatar\nmissing", fill="black", font=body_font)

    # Text area (right)
    draw.text((420, 230), f"This certificate is proudly awarded to:", fill=(30,30,30), font=body_font)
    draw.text((420, 300), f"⭐ {name} ⭐", fill=(10,70,180), font=title_font)
    draw.text((420, 420), "For bravely helping Santa,\nrescuing the reindeer,\nfixing the sleigh,\nand saving Christmas!", fill=(30,30,30), font=body_font)

    # Footer signature
    draw.text((420, 620), "Santa Claus 🎅", fill=(80,0,0), font=body_font)
    return cert

def pil_image_to_bytes(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf

# ---------- Game Layout ----------
st.markdown("<h1 style='text-align:center;'>🎄 Rowan's Christmas Adventure — Animated</h1>", unsafe_allow_html=True)

left, right = st.columns([2,1])

with left:
    # Scene rendering area
    scene = st.session_state.scene

    # Determine background & text
    if scene == "intro":
        st.image(BG_GARAGE, use_column_width=True)
        st.markdown("### It's Christmas Eve! Santa's sleigh needs help. Ready to be Rowan the hero?")
        if st.button("Start the Adventure! 🎅✨"):
            play_sound_html(SND_BELL)
            go("garage")
    elif scene == "garage":
        # Show animated area with avatar and a garage background
        st.markdown("### Garage — choose a racer and **drive** to the Candy Cane Forest.")
        # controls
        car1, car2, car3 = st.columns(3)
        with car1:
            st.button("Red Racer 🚗", on_click=lambda: go("forest", action="drive"))
        with car2:
            st.button("Green Turbo 🚗", on_click=lambda: go("forest", action="drive"))
        with car3:
            st.button("Blue Speedster 🚗", on_click=lambda: go("forest", action="drive"))

        # show the animated garage scene (no need to animate on this screen)
        st.image(BG_GARAGE, use_column_width=True)

    elif scene == "forest":
        st.markdown("### Candy Cane Forest — Donkey Kong is here to help! Choose to **walk** with DK or **race** to find the reindeer.")
        choice1, choice2 = st.columns(2)
        with choice1:
            st.button("Walk with Donkey Kong 🐵", on_click=lambda: go("find_reindeer", action="walk"))
        with choice2:
            st.button("Drive (fast!) 🚗", on_click=lambda: go("find_reindeer", action="drive"))

        # Render an interactive animated scene where the avatar either walks or drives
        # We embed HTML/CSS that moves the avatar image across the background when `action` is set.
        action = st.session_state.action
        bg = BG_FOREST
        avatar_url = f"file://{AVATAR_PATH}" if Path(AVATAR_PATH).exists() else ""
        # unique key to force re-run animation when timestamp changes
        anim_key = int(st.session_state.last_move)

        html = f"""
        <div style="position:relative; width:100%; height:420px; background-image:url('{bg}'); background-size:cover; border-radius:8px; overflow:hidden;">
            <style>
                .avatar {{
                    width:160px;
                    position:absolute;
                    bottom:20px;
                    left:20px;
                    transition: transform 1s linear;
                }}
                /* walking animation: small bob + slow move */
                .walk {{
                    animation: bob 0.6s ease-in-out infinite;
                    transform: translateX(420px);
                }}
                /* driving animation: faster, smoother */
                .drive {{
                    transform: translateX(760px);
                    transition: transform 2s cubic-bezier(.2,.9,.2,1);
                }}
                @keyframes bob {{
                    0% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-10px); }}
                    100% {{ transform: translateY(0); }}
                }}
            </style>
            <img id="avatar_{anim_key}" class="avatar {'walk' if action=='walk' else ('drive' if action=='drive' else '')}" src="{avatar_url}" />
        </div>
        """
        components.html(html, height=440)

        # Play appropriate sound once after action triggered
        if action == "walk":
            play_sound_html(SND_MAGIC)
        elif action == "drive":
            play_sound_html(SND_ENGINE)

        st.caption("If the avatar didn't move, press the choice again to retrigger the animation.")

    elif scene == "find_reindeer":
        st.markdown("### You found the reindeer! Now the sleigh is broken — choose a magical tool to fix it.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Star Hammer ✨", on_click=lambda: go("sleigh_fixed"))
        with col2:
            st.button("Light Blade ⚔️", on_click=lambda: go("sleigh_fixed"))
        with col3:
            st.button("Spark Wand 💫", on_click=lambda: go("sleigh_fixed"))

        # show the forest background
        st.image(BG_FOREST, use_column_width=True)

    elif scene == "sleigh_fixed":
        st.markdown("### Sleigh Fixed! Fly to deliver the present.")
        if st.button("Fly to the rooftop 🎁"):
            play_sound_html(SND_BELL)
            go("deliver", action="fly")
        st.image(BG_GARAGE, use_column_width=True)

    elif scene == "deliver":
        st.markdown("### Deliver the Present — you're almost done!")
        # show rooftop bg and animate avatar flying across
        avatar_url = f"file://{AVATAR_PATH}" if Path(AVATAR_PATH).exists() else ""
        html = f"""
        <div style="position:relative; width:100%; height:420px; background-image:url('{BG_ROOFTOP}'); background-size:cover; border-radius:8px; overflow:hidden;">
            <style>
                .avatarfly {{ width:140px; position:absolute; left: -160px; top: 40px; transform: rotate(-10deg); transition: transform 2s linear, left 2s linear; }}
                .flyto {{ left: 820px; transform: rotate(0deg); }}
            </style>
            <img id="avatar_fly_{int(st.session_state.last_move)}" class="avatarfly {'flyto' if st.session_state.action=='fly' else ''}" src="{avatar_url}" />
        </div>
        """
        components.html(html, height=440)
        if st.session_state.action == "fly":
            play_sound_html(SND_MAGIC)

        if st.button("Finish Mission 🎄"):
            go("ending")

    elif scene == "ending":
        st.markdown("## 🎉 Hooray — Rowan saved Christmas! ⭐")
        st.image(BG_ROOFTOP, use_column_width=True)
        st.write("Santa awards him the **Christmas Hero Medal**!")

        # create certificate image
        try:
            cert_img = make_certificate(AVATAR_PATH, name="ROWAN")
            buf = pil_image_to_bytes(cert_img)
            st.download_button("Download Rowan’s Certificate (PNG) 🏅", data=buf, file_name="Rowan_Christmas_Certificate.png", mime="image/png")
        except Exception as e:
            st.write("Couldn't make certificate automatically (avatar file missing).")

        if st.button("Play Again 🔁"):
            go("intro")

with right:
    # Side panel: instructions and avatar preview
    st.sidebar.title("Game Controls & Tips")
    st.sidebar.write("""
    - Click the big choices to trigger animated walk/drive.
    - If animation doesn't run, press the same choice again to retrigger.
    - Replace avatar or background images by editing the constants at top of the script.
    """)
    if Path(AVATAR_PATH).exists():
        st.sidebar.image(AVATAR_PATH, caption="Rowan (avatar preview)")
    else:
        st.sidebar.write("Avatar image not found at the configured path.")

    st.sidebar.markdown("---")
    st.sidebar.write("Want these enhancements?")
    st.sidebar.write("- Add richer sprite-sheet walking animation (I can provide).")
    st.sidebar.write("- Add Lottie/animated vector assets for smoother motion.")
    st.sidebar.write("- Replace sounds with a background K-Pop instrumental loop (kid-friendly).")
