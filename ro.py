import streamlit as st
import base64

st.set_page_config(page_title="Rowan's Christmas Adventure 🎄", layout="centered")

# ------------------------------
# Initialization
# ------------------------------
if "scene" not in st.session_state:
    st.session_state.scene = "intro"

def go(scene):
    st.session_state.scene = scene

# ------------------------------
# Utility: Play Sound
# ------------------------------
def play_sound(sound_url):
    audio_html = f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ------------------------------
# Utility: Certificate Download
# ------------------------------
def certificate():
    cert_text = f"""
    🎄 CHRISTMAS HERO AWARD 🎄

    This certificate is proudly awarded to:

    ⭐ ROWAN ⭐

    For bravely helping Santa,
    rescuing the reindeer,
    fixing the sleigh,
    racing through Candy Cane Forest,
    and saving Christmas!

    You are an official
    🎅 CHRISTMAS HERO 🎅
    """

    b = cert_text.encode("utf-8")
    return b

# ------------------------------
# Title
# ------------------------------
st.markdown("<h1 style='text-align:center;'>🎄 Rowan’s Christmas Adventure 🎁</h1>", unsafe_allow_html=True)

# ------------------------------
# SCENES
# ------------------------------

# --- INTRO ---
if st.session_state.scene == "intro":
    st.image("https://i.imgur.com/WPj3w5A.png")
    st.write("**It’s Christmas Eve… and Santa needs a hero. Is Rowan ready?**")

    play_sound("https://www.myinstants.com/media/sounds/christmas-bells.mp3")

    st.button("Yes! 🎅✨", on_click=lambda: go("garage"))


# --- CAR GARAGE (cars theme) ---
elif st.session_state.scene == "garage":
    st.image("https://i.imgur.com/Br6sz5Q.png")  # cute cartoon garage
    st.write("**Rowan zooms into Santa’s Magical Car Garage!**")
    st.write("One of the reindeer got lost — Rowan must drive a Christmas Racer to find them!")

    play_sound("https://www.myinstants.com/media/sounds/car-starting.mp3")

    st.button("Start the Racer 🚗💨", on_click=lambda: go("choose_car"))


# --- Choose car (kid-friendly cars theme) ---
elif st.session_state.scene == "choose_car":
    st.write("**Which Christmas Racer should Rowan drive?**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://i.imgur.com/auZfjBw.png")  # red car
        st.button("❤️ Red Racer", on_click=lambda: go("forest_intro"))

    with col2:
        st.image("https://i.imgur.com/JJran4k.png")  # green car
        st.button("💚 Green Turbo", on_click=lambda: go("forest_intro"))

    with col3:
        st.image("https://i.imgur.com/8zdUCkw.png")  # blue
        st.button("💙 Blue Snow Speedster", on_click=lambda: go("forest_intro"))


# --- Candy Forest (Donkey Kong style) ---
elif st.session_state.scene == "forest_intro":
    st.image("https://i.imgur.com/0Z9QKsD.png")
    st.write("**Rowan drives into the Candy Cane Forest… and suddenly— DONKEY KONG appears!**")
    st.write("He’s friendly and wants to help find the missing reindeer!")

    play_sound("https://www.myinstants.com/media/sounds/dk-barrel.mp3")

    st.button("Team up with Donkey Kong 🐵✨", on_click=lambda: go("dk_scene"))


# --- DK SCENE ---
elif st.session_state.scene == "dk_scene":
    st.image("https://i.imgur.com/6X7Iltp.png")
    st.write("**Donkey Kong points to two paths. Which way should Rowan go?**")

    col1, col2 = st.columns(2)
    with col1:
        st.button("🍌 Banana Road", on_click=lambda: go("find_reindeer"))
    with col2:
        st.button("🎄 Christmas Tree Trail", on_click=lambda: go("find_reindeer"))


# --- FIND REINDEER ---
elif st.session_state.scene == "find_reindeer":
    st.image("https://i.imgur.com/WXf2pIc.png")
    st.write("**Rowan finds the missing reindeer playing in the snow!**")

    play_sound("https://www.myinstants.com/media/sounds/magic-wand-1.mp3")

    st.button("Take reindeer back ➡️", on_click=lambda: go("sleigh_broken"))


# --- Broken sleigh (K-Pop Demon Hunter energy, kid-safe) ---
elif st.session_state.scene == "sleigh_broken":
    st.image("https://i.imgur.com/KJq2z6K.png")
    st.write("**Oh no! Santa’s sleigh is broken!**")
    st.write("Rowan must choose a magical K-Pop Demon Hunter tool to repair it ✨⚔️")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("✨ Star Hammer", on_click=lambda: go("sleigh_fixed"))
    with col2:
        st.button("⚔️ Light Blade", on_click=lambda: go("sleigh_fixed"))
    with col3:
        st.button("💫 Spark Wand", on_click=lambda: go("sleigh_fixed"))


# --- Sleigh fixed ---
elif st.session_state.scene == "sleigh_fixed":
    st.image("https://i.imgur.com/kWuk2Uq.png")
    st.write("**The sleigh is fixed! Time to deliver the present!**")

    play_sound("https://www.myinstants.com/media/sounds/sparkle.mp3")

    st.button("Fly to the house 🎁", on_click=lambda: go("deliver"))


# --- Deliver present ---
elif st.session_state.scene == "deliver":
    st.image("https://i.imgur.com/k6k4QNk.png")
    st.write("**Rowan gently places the present under the tree…**")

    st.button("Finish Mission 🎄", on_click=lambda: go("ending"))


# --- Ending & Certificate ---
elif st.session_state.scene == "ending":
    st.image("https://i.imgur.com/9M9D4x6.png")
    st.markdown("## 🎉 Rowan saved Christmas! ⭐")
    st.write("Santa awards him the **Christmas Hero Medal**!")

    st.download_button(
        "Download Rowan’s Certificate 🏅",
        certificate(),
        file_name="Rowan_Christmas_Hero_Certificate.txt"
    )

    st.button("Play Again 🔁", on_click=lambda: go("intro"))
