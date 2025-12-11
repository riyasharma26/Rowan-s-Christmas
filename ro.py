# rowans_christmas_adventure.py
# Rowan's Christmas Adventure – Big Emoji Edition

import streamlit as st
import random
import time

st.set_page_config(page_title="Rowan's Christmas Adventure",
                   layout="wide",
                   initial_sidebar_state="collapsed")

# --------------------------
# Custom CSS
# --------------------------
PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

html, body, [data-testid="stAppViewContainer"] > .main {
  height: 100%;
  background: linear-gradient(180deg, #d8ffe3, #ffefef);
  font-family: 'Bangers', sans-serif;
}

/* Bubble title */
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

/* Game column */
.left {
  position: relative;
  padding: 20px;
  border-radius: 25px;
  background: rgba(255,255,255,0.5);
  border: 6px solid #ffffff;
  box-shadow: 0 8px 40px rgba(0,0,0,0.08);
}

/* Right mission list */
.right {
  background: rgba(255,255,255,0.75);
  border-radius: 22px;
  padding: 1rem 1.2rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.05);
}

/* Mission */
.mission {
  font-size: 1.7rem;
  padding: 14px;
  margin-bottom: 10px;
  border-radius: 14px;
  display: flex;
  justify-content: space-between;
  background: #ffffffc9;
}

/* Emoji sizes */
.big-emoji { font-size: 6rem; }
.big-emoji-med { font-size: 4rem; }
.big-emoji-sm { font-size: 3rem; }

/* Hiding footer/header */
header, footer {visibility: hidden;}

@keyframes fall {
  0% { transform: translateY(-10%); }
  100% { transform: translateY(110%); }
}
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
left, right = st.columns([3, 1], gap="large")

# --------------------------
# LEFT PANEL (GAME)
# --------------------------
with left:
    st.markdown("<div class='left'>", unsafe_allow_html=True)

    # ❄️ Fewer Floating Snowflakes — only 3 now
    snow_html = "<div style='position:absolute;inset:0;z-index:-1;'>"
    for i in range(3):
        left_pos = random.randint(1, 95)
        delay = random.uniform(0, 3)
        dur = random.uniform(5, 10)
        snow_html += f"""
        <div style='position:absolute;left:{left_pos}%;top:-10%;
                     animation: fall {dur}s linear {delay}s infinite;
                     font-size:5rem;'>❄️</div>
        """
    snow_html += "</div>"
    st.markdown(snow_html, unsafe_allow_html=True)

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
        if c1.button("🌲\nDecorate", use_container_width=True,
                     disabled=st.session_state.missions_completed["Decorate the Tree"]):
            st.session_state.stage = "decorate"
            st.rerun()

        if c2.button("❄️\nCatch", use_container_width=True,
                     disabled=st.session_state.missions_completed["Catch Snowflakes"]):
            st.session_state.stage = "catch"
            st.rerun()

        if c3.button("🎁\nFind", use_container_width=True,
                     disabled=st.session_state.missions_completed["Find the Present"]):
            st.session_state.stage = "find"
            st.rerun()

        total_done = sum(st.session_state.missions_completed.values())
        st.markdown(
            f"<div style='text-align:center;font-size:2rem;margin-top:1rem;'>Completed: {total_done}/3</div>",
            unsafe_allow_html=True)

    # --------------------------
    # DECORATE THE TREE
    # --------------------------
    elif st.session_state.stage == "decorate":
        st.markdown("<div style='text-align:center;font-size:4rem;'>🌲 Decorate the Tree</div>",
                    unsafe_allow_html=True)
        st.markdown(kid_msg("Place all three ornaments!", "✨"), unsafe_allow_html=True)

        left_spot = "🔴" if st.session_state.ornaments["red"] else "⚪"
        mid_spot = "🔵" if st.session_state.ornaments["blue"] else "⚪"
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
            if col1.button("🔴", use_container_width=True):
                st.session_state.ornaments["red"] = True
                st.rerun()
        if not st.session_state.ornaments["blue"]:
            if col2.button("🔵", use_container_width=True):
                st.session_state.ornaments["blue"] = True
                st.rerun()
        if not st.session_state.ornaments["gold"]:
            if col3.button("🟡", use_container_width=True):
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
    # SNOWFLAKE CATCH GAME
    # --------------------------
    elif st.session_state.stage == "catch":

        st.markdown("<h2 style='font-size: 50px; text-align:center;'>❄️ Catch the Falling Snowflakes! ❄️</h2>",
                    unsafe_allow_html=True)

        st.write("Tap **CATCH!** when the snowflake reaches the bottom!")

        game_area = st.empty()
        caught_display = st.empty()
        catch_button = st.button("❄️ CATCH! ❄️", use_container_width=True)

        if "flake_y" not in st.session_state:
            st.session_state.flake_y = 0
        if "flake_x" not in st.session_state:
            st.session_state.flake_x = random.randint(0, 10)
        if "caught" not in st.session_state:
            st.session_state.caught = 0

        for frame in range(50):
            grid = ""
            for y in range(10):
                row = ""
                for x in range(11):
                    if x == st.session_state.flake_x and y == st.session_state.flake_y:
                        row += "<span style='font-size:80px;'>❄️</span>"
                    else:
                        row += "<span style='font-size:80px;'>&nbsp;</span>"
                grid += row + "<br>"

            game_area.markdown(grid, unsafe_allow_html=True)

            if catch_button and st.session_state.flake_y == 9:
                st.session_state.caught += 1
                caught_display.markdown(
                    f"<h3 style='color:green;'>Caught: {st.session_state.caught}</h3>",
                    unsafe_allow_html=True)
                st.session_state.flake_y = 0
                st.session_state.flake_x = random.randint(0, 10)
                st.rerun()

            st.session_state.flake_y += 1
            if st.session_state.flake_y > 9:
                st.session_state.flake_y = 0
                st.session_state.flake_x = random.randint(0, 10)
                st.rerun()

            time.sleep(0.15)

        if st.session_state.caught >= 3:
            st.session_state.missions_completed["Catch Snowflakes"] = True
            st.balloons()
            st.markdown(kid_msg("Amazing catching!!", "🎉"), unsafe_allow_html=True)
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
        st.markdown("<div style='text-align:center;font-size:4rem;'>🎁 Find the Present</div>",
                    unsafe_allow_html=True)
        st.markdown(kid_msg("Pick ONE present!", "✨"), unsafe_allow_html=True)

        correct = st.session_state.get("_correct_present", random.randint(1, 3))
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
                st.markdown(kid_msg("You found the secret present!!", "🎉"), unsafe_allow_html=True)
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
# RIGHT PANEL (MISSIONS)
# --------------------------
with right:
    st.markdown("<div class='right'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:2.2rem;margin-bottom:1rem;'>Missions</div>",
                unsafe_allow_html=True)

    for name, done in st.session_state.missions_completed.items():
        mark = "✅" if done else "•"
        st.markdown(
            f"<div class='mission'>{name} <span class='big-emoji-sm'>{mark}</span></div>",
            unsafe_allow_html=True)

    if all(st.session_state.missions_completed.values()):
        st.markdown("<div style='font-size:2rem;text-align:center;margin-top:1rem;'>🎉 ALL DONE!</div>",
                    unsafe_allow_html=True)
        if st.button("Play Again"):
            reset_game()
            st.rerun()

    if st.button("Reset Game"):
        reset_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
