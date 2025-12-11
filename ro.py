import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Rowan's Christmas Adventure", layout="centered")

# --- TITLE BUBBLE ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #ff3c7d, #ffa33a);
    padding: 25px;
    border-radius: 30px;
    text-align:center;
    font-size: 40px;
    font-weight: 700;
    color: white;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.25);
    letter-spacing: 2px;">
    ROWAN'S CHRISTMAS ADVENTURE
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- Stick Figure Rowan (drawn in Python) ---
def draw_rowan():
    img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse((110, 40, 190, 120), fill="#f7d29a", outline="black", width=3)

    # Hair (brown)
    d.arc((100, 20, 200, 100), start=0, end=180, fill="#744b20", width=15)

    # Body
    d.line((150, 120, 150, 210), fill="black", width=6)

    # Arms
    d.line((150, 140, 110, 190), fill="black", width=6)
    d.line((150, 140, 190, 190), fill="black", width=6)

    # Legs
    d.line((150, 210, 120, 260), fill="black", width=6)
    d.line((150, 210, 180, 260), fill="black", width=6)

    return img

st.image(draw_rowan(), caption="Rowan the Adventurer!", width=250)

st.write("## ❄️ Mission: Help Rowan Find Santa's Magic Star!")
st.write("""
Rowan must press the button to **light the Christmas Star**  
and save Santa's sleigh from getting stuck in the snow!
""")

# Store mission completion
if "won" not in st.session_state:
    st.session_state.won = False

# --- Main Button ---
if not st.session_state.won:
    if st.button("🌟 Press to Light the Christmas Star!"):
        st.session_state.won = True
        st.success("🎉 Rowan did it! The star is shining and Santa is ready!")
else:
    st.markdown("### ⭐ Mission Complete! ⭐")
    st.balloons()

    # --- CERTIFICATE GENERATOR ---
    def create_certificate(name="ROWAN"):
        W, H = 1000, 700
        cert = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(cert)

        # Fonts
        try:
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
            main_font = ImageFont.truetype("DejaVuSans.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            main_font = ImageFont.load_default()

        # Header banner
        d.rectangle([(0,0),(W,150)], fill=(255,80,120))
        d.text((W//2, 40), "CHRISTMAS HERO AWARD", font=title_font, fill="white", anchor="mm")

        # Stick figure Rowan
        avatar = draw_rowan().resize((250,250))
        cert.paste(avatar, (60, 250), avatar)

        # Text
        d.text((350,250), f"This certificate is awarded to", fill=(0,0,0), font=main_font)
        d.text((350,310), f"{name}", fill=(0,70,170), font=title_font)
        d.text((350,410),
               "For lighting Santa’s Magic Star,\nsaving the Christmas sleigh,\nand being an amazing helper!",
               fill=(0,0,0), font=main_font)

        # Santa signature
        d.text((350,560), "🎅 Santa Claus", font=main_font, fill=(120,0,0))

        # Export to buffer
        buf = io.BytesIO()
        cert.save(buf, format="PNG")
        buf.seek(0)
        return buf

    st.write("### 🎁 Download Rowan's Certificate")
    cert = create_certificate("ROWAN")
    st.download_button(
        label="📜 Download Certificate",
        data=cert,
        file_name="Rowan_Christmas_Certificate.png",
        mime="image/png"
    )
