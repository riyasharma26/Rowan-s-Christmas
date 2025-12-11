# rowans_christmas_adventure.py
# Rowan's Christmas Adventure (Large Emoji Edition, fixed)
# Streamlit mini-game for a 4-year-old
# Run: streamlit run rowans_christmas_adventure.py

import streamlit as st
import random
import time

st.set_page_config(page_title="Rowan's Christmas Adventure", layout="wide", initial_sidebar_state="collapsed")

# --------------------------
# Custom styling for BIG emojis and bright kid UI
# Includes falling snowflake keyframes used in the Catch mission
# --------------------------
PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

html, body, [data-testid="stAppViewContainer"] > .main {
  height: 100%;
  background: linear-gradient(180deg, #d8ffe3, #ffefef);
  font-family: 'Bangers', sans-serif;
}

/* Big bubble title */
.title {
  font-size: 5.5rem;
  text-align: center;
  color: #8b2a1d;
  text-shadow: 3px 3px 0 #fff, 6px 6px 0 rgba(0,0,0,0.1);
  margin-bottom: 0.2rem;
}

.subtitle {
  font-size: 2rem;
  text-align: center;
  color: #145022;
  margin-bottom: 0.6rem;
}

/* Left panel */
.left {
  position: relative;
  min-height: 540px;
}

/* Mission panel */
.right {
  background: rgba(255,255,255,0.75);
  border-radius: 22px;
  padding: 1rem 1.2rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.05);
}

/* Mission items */
.mission {
  font-size: 1.7rem;
  padding: 14px;
  margin-bottom: 10px;
  border-radius: 14px;
  display: flex;
  justify-content: space-between;
  background: #ffffffc9;
}

.pulse {
  animation: pulse 1.4s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); }
  70% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

/* Big click buttons */
.big-btn {
  font-size: 3rem;
  padding: 24px 34px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  font-family: 'Bangers';
}

/* HUGE emoji size */
.big-emoji {
  font-size: 6rem;     /* 4× normal */
  line-height: 1.0;
}

.big-emoji-med {
  font-size: 4rem;
}

.big-emoji-sm {
  font-size: 3rem;
}

/* Snowflake falling animation (used in the Catch mission) */
.fall-container {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
  border-radius: 18px;
  margin: 8px 0 12px 0;
  background: linear-gradient(180deg,#f8ffff, #e6f7ff);
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}
.snow {
  position: absolute;
  top: -10%;
  font-size: 5rem; /* large snowflake size */
  opacity: 0.95;
  will-change: transform;
  animation-name: fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  filter: drop-shadow(0 6px 6px rgba(0,0,0,0.08));
}
@keyframes fall {
  0% { transform: translateY(-15vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(120vh) rotate(360deg); opacity: 0.9; }
}

/* Hide footer/header */
header, footer {visibility: hidden;}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)


# --------------------------
# State initialization
# --------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "welcome"
if "ornaments" not in st.session_state:
    st.session_state.ornaments = {"red": False, "blue": False, "gold": False}
if "caught_count" not in st.session_state:
    st.session_state.caught_count = 0
if "find_choice" not in st.session_state:
    st.session_state.find_choice = None
if "missions_completed" not in st.session_state:
    st.session_state.missions_completed = {
        "Decorate the Tree": False,
        "Catch Snowflakes": False,
        "Find the Present": False
    }

def reset_game():
    st.session_state.stage = "welcome"
    st.session_state.ornaments = {"red": False, "blue": False, "gold": False}
    st.session_state.caught_count = 0
    st.session_state.find_choice = None
    st.session_state.missions_completed = {
        "Decorate the Tree": False,
        "Catch Snowflakes": False,
        "Find the Present": False
    }

def kid_msg(text, emoji="✨"):
    return f"<div style='font-size:2rem;text-align:center;color:#333;'>{emoji} <b>{text}</b> {emoji}</div>"


# --------------------------
# HEADER
# --------------------------
st.markdown("<div class='title'>Rowan's Christmas Adventure</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A big, colorful adventure made just for Rowan! 🎄</div>", unsafe_allow_html=True)


# --------------------------
# MAIN LAYOUT
# --------------------------
left, right = st.columns([3,1], gap="large")

with left:
    st.markdown("<div class='left'>", unsafe_allow_html=True)

    # ❄️ Decorative floating snowflakes behind content (non-interactive)
    deco_snow = "<div style='position:absolute;inset:0;z-index:-1;'>"
    for i in range(6):
        left_pos = random.randint(1, 95)
        delay = round(random.uniform(0, 4), 2)
        dur = round(random.uniform(6, 14), 2)
        size = random.choice(["4.2rem", "4.8rem", "5.2rem"])
        deco_snow += f"""
        <div style='position:absolute;left:{left_pos}%;top:-10%;
                     animation: fall {dur}s linear {delay}s infinite;
                     font-size:{size};opacity:0.9;'>❄️</div>
        """
    deco_snow += "</div>"
    st.markdown(deco_snow, unsafe_allow_html=True)

    # --------------------------
    # WELCOME SCREEN
    # --------------------------
    if st.session_state.stage == "welcome":
        st.markdown(kid_msg("Hi Rowan! Are you ready to play?", "🎅"), unsafe_allow_html=True)
        if st.button("START 🎄", use_container_width=True):
            st.session_state.stage = "game"
            st.rerun()

    # --------------------------
    # MISSION SELECT
    # --------------------------
    elif st.session_state.stage == "game":
        st.markdown("<div style='text-align:center;font-size:3rem;margin:1rem 0;'>Choose a Mission!</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button("🌲\nDecorate", use_container_width=True, help="Decorate", disabled=st.session_state.missions_completed["Decorate the Tree"]):
            st.session_state.stage = "decorate"
            st.rerun()
        if c2.button("❄️\nCatch", use_container_width=True, disabled=st.session_state.missions_completed["Catch Snowflakes"]):
            st.session_state.stage = "catch"
            st.rerun()
        if c3.button("🎁\nFind", use_container_width=True, disabled=st.session_state.missions_completed["Find the Present"]):
            st.session_state.stage = "find"
            st.rerun()

        total_done = sum(st.session_state.missions_completed.values())
        st.markdown(f"<div style='text-align:center;font-size:2rem;margin-top:1rem;'>Completed: {total_done}/3</div>", unsafe_allow_html=True)

    # --------------------------
    # DECORATE THE TREE
    # --------------------------
    elif st.session_state.stage == "decorate":
        st.markdown("<div style='text-align:center;font-size:4rem;'>🌲 Decorate the Tree</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Place all three ornaments!", "✨"), unsafe_allow_html=True)

        # Show tree with HUGE emojis
        left_spot = "🔴" if st.session_state.ornaments["red"] else "⚪"
        mid_spot  = "🔵" if st.session_state.ornaments["blue"] else "⚪"
        right_spot = "🟡" if st.session_state.ornaments["gold"] else "⚪"

        st.markdown(f"""
        <div style='text-align:center; margin-top:1rem;'>
            <div class='big-emoji'>🌲</div>
            <div style='font-size:6rem;'>{left_spot} {mid_spot} {right_spot}</div>
            <div class='big-emoji'>⭐</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        if not st.session_state.ornaments["red"]:
            if col1.button("🔴", help="Red ornament", use_container_width=True):
                st.session_state.ornaments["red"] = True
                st.rerun()
        if not st.session_state.ornaments["blue"]:
            if col2.button("🔵", help="Blue ornament", use_container_width=True):
                st.session_state.ornaments["blue"] = True
                st.rerun()
        if not st.session_state.ornaments["gold"]:
            if col3.button("🟡", help="Gold ornament", use_container_width=True):
                st.session_state.ornaments["gold"] = True
                st.rerun()

        if all(st.session_state.ornaments.values()):
            st.session_state.missions_completed["Decorate the Tree"] = True
            st.balloons()
            st.markdown(kid_msg("Beautiful tree, Rowan!", "🌟"), unsafe_allow_html=True)
            if st.button("Back to Missions"):
                st.session_state.stage = "game"
                st.rerun()

        if st.button("Back"):
            st.session_state.stage = "game"
            st.rerun()

    # --------------------------
    # CATCH SNOWFLAKES (with CSS-animated falling snowflakes)
    # --------------------------
    elif st.session_state.stage == "catch":
        st.markdown("<div style='text-align:center;font-size:4rem;'>❄️ Catch Snowflakes!</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Catch 3 giant snowflakes! Tap CATCH when you see one you like.", "☃️"), unsafe_allow_html=True)

        # Show a container with many css-animated snowflake emojis (purely visual)
        snow_container_html = "<div class='fall-container'>"
        for i in range(12):
            left_pos = random.randint(2, 94)
            delay = round(random.uniform(0, 5), 2)
            dur = round(random.uniform(6, 14), 2)
            size = random.choice(["4.2rem", "4.8rem", "5.2rem"])
            # alternate small horizontal drift using translateX via animation-delay stagger to vary motion
            snow_container_html += f"<div class='snow' style='left:{left_pos}%; animation-duration:{dur}s; animation-delay:{delay}s; font-size:{size};'>❄️</div>"
        snow_container_html += "</div>"
        st.markdown(snow_container_html, unsafe_allow_html=True)

        # Big catch button — keep gameplay simple and fun for a 4-year-old
        caught = st.button("CATCH ❄️", use_container_width=True)
        if caught:
            # high success chance so it stays fun
            if random.random() < 0.92:
                st.session_state.caught_count += 1
                st.success(f"Nice catch! ❄️ {st.session_state.caught_count}/3")
            else:
                st.info("Oh no, it slipped away! Try again!")

        st.markdown(f"<div style='text-align:center;font-size:2rem;margin-top:8px;'>Snowflakes caught: <b>{st.session_state.caught_count}</b> / 3</div>", unsafe_allow_html=True)

        if st.session_state.caught_count >= 3:
            st.session_state.missions_completed["Catch Snowflakes"] = True
            st.balloons()
            st.markdown(kid_msg("You caught them all! Great job!", "❄️"), unsafe_allow_html=True)
            if st.button("Back to Missions"):
                st.session_state.stage = "game"
                st.rerun()

        if st.button("Back"):
            st.session_state.stage = "game"
            st.rerun()

    # --------------------------
    # FIND THE PRESENT
    # --------------------------
    elif st.session_state.stage == "find":
        st.markdown("<div style='text-align:center;font-size:4rem;'>🎁 Find the Present</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Pick ONE present!", "✨"), unsafe_allow_html=True)

        correct = st.session_state.get("_correct_present", random.randint(1,3))
        st.session_state._correct_present = correct

        c1, c2, c3 = st.columns(3)
        if c1.button("🎁", use_container_width=True):
            st.session_state.find_choice = 1
        if c2.button("🎀", use_container_width=True):
            st.session_state.find_choice = 2
        if c3.button("🧸", use_container_width=True):
            st.session_state.find_choice = 3

        if st.session_state.find_choice is not None:
            if st.session_state.find_choice == correct:
                st.session_state.missions_completed["Find the Present"] = True
                st.balloons()
                st.markdown(kid_msg("You found it!!", "🎉"), unsafe_allow_html=True)
                st.markdown("<div style='text-align:center;font-size:4rem;'>🧸</div>", unsafe_allow_html=True)
                if st.button("Back to Missions"):
                    st.session_state.stage = "game"
                    st.rerun()
            else:
                st.markdown(kid_msg("Try again!", "😅"), unsafe_allow_html=True)
                if st.button("Try again"):
                    st.session_state.find_choice = None
                    st.rerun()

        if st.button("Back"):
            st.session_state.stage = "game"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------
# RIGHT PANEL – MISSION LIST
# --------------------------
with right:
    st.markdown("<div class='right'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:2.2rem;margin-bottom:1rem;'>Missions</div>", unsafe_allow_html=True)

    for name, done in st.session_state.missions_completed.items():
        mark = "✅" if done else "•"
        st.markdown(f"<div class='mission'>{name} <span class='big-emoji-sm'>{mark}</span></div>",
                    unsafe_allow_html=True)

    if all(st.session_state.missions_completed.values()):
        st.markdown("<div style='font-size:2rem;text-align:center;margin-top:1rem;'>🎉 ALL DONE!</div>", unsafe_allow_html=True)
        if st.button("Play Again"):
            reset_game()
            st.rerun()

    if st.button("Reset Game"):
        reset_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
