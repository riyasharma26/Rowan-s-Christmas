# rowans_christmas_adventure.py
# Rowan's Christmas Adventure
# Single-file Streamlit app for a 4-year-old mini-game
# Run: streamlit run rowans_christmas_adventure.py

import streamlit as st
import random
import time

st.set_page_config(page_title="Rowan's Christmas Adventure", layout="wide", initial_sidebar_state="collapsed")

# --------------------------
# Page styling (big, colorful, no boxes)
# --------------------------
PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

html, body, [data-testid="stAppViewContainer"] > .main {
  height: 100%;
  background: radial-gradient(circle at 20% 10%, #f0fff4 0%, #dfffe0 10%, #eaf9ff 30%, #ffefef 100%);
  font-family: 'Bangers', sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Make everything centered and full-bleed */
.main > div {
  padding: 0rem 1rem 3rem 1rem;
}

/* Big bubble title */
.title {
  font-family: 'Bangers', 'Comic Sans MS', cursive;
  font-size: 5.2rem;
  text-align: center;
  margin: 0.4rem 0 0.2rem 0;
  color: #7b2a1d;
  text-shadow: 2px 2px 0 #fff, 6px 6px 0 rgba(0,0,0,0.06);
}

/* subtitle */
.subtitle {
  text-align: center;
  font-size: 1.6rem;
  margin-bottom: 0.6rem;
  color: #124d1f;
}

/* Full-screen game area */
.game-area {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
  margin-top: 0.6rem;
}

/* Left panel big area - no boxes */
.left {
  flex: 1;
  min-height: 540px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* Right panel for missions list */
.right {
  width: 360px;
  min-height: 420px;
  border-radius: 22px;
  padding: 1rem 1.2rem;
  background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(255,255,255,0.60));
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* Mission item */
.mission {
  font-family: 'Bangers', sans-serif;
  font-size: 1.35rem;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(90deg, #fff, #f4fff6);
}

/* Pulsing for active mission */
.pulse {
  animation: pulse 1.4s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0,0,0,0.05); }
  70% { transform: scale(1.02); box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0,0,0,0.05); }
}

/* Big round buttons */
.big-btn {
  font-size: 2rem;
  padding: 18px 28px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  outline: none;
  box-shadow: 0 8px 22px rgba(0,0,0,0.12);
  transition: transform .12s;
  font-family: 'Bangers', sans-serif;
}
.big-btn:active { transform: translateY(2px); }

/* Tree area */
.tree {
  width: 380px;
  height: 480px;
  border-radius: 22px;
  display:flex;
  align-items:center;
  justify-content:center;
  position: relative;
}

/* Snowflake animation */
.snowflake {
  position: absolute;
  top: -10%;
  font-size: 2.2rem;
  animation: fall linear infinite;
  opacity: .9;
  filter: drop-shadow(0 4px 4px rgba(0,0,0,0.12));
}
@keyframes fall {
  0% { transform: translateY(-10vh) rotate(0deg); }
  100% { transform: translateY(110vh) rotate(360deg); }
}

/* Confetti celebration */
.confetti {
  pointer-events: none;
  position: absolute;
  inset: 0;
}
.confetti i {
  position: absolute;
  font-style: normal;
  animation: confetti-fall linear infinite;
  transform-origin: center;
}
@keyframes confetti-fall {
  0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(110vh) rotate(540deg); opacity: 0.6; }
}

/* Present buttons */
.present {
  font-size: 2.4rem;
  padding: 10px 14px;
  border-radius: 18px;
  cursor: pointer;
  border: none;
}

/* small helper text */
.hint {
  text-align:center;
  font-size:1.25rem;
  margin-top: 0.6rem;
  color:#3b3b3b;
}

/* Hide Streamlit's default header & footer */
header, footer {visibility: hidden;}
</style>
"""

st.markdown(PAGE_CSS, unsafe_allow_html=True)

# --------------------------
# Helper functions & state
# --------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "welcome"  # welcome, game, decorate, catch, find, finished
if "ornaments" not in st.session_state:
    # three ornaments to place
    st.session_state.ornaments = {"red": False, "blue": False, "gold": False}
if "caught_count" not in st.session_state:
    st.session_state.caught_count = 0
if "find_choice" not in st.session_state:
    st.session_state.find_choice = None
if "missions_completed" not in st.session_state:
    st.session_state.missions_completed = {"Decorate the Tree": False, "Catch Snowflakes": False, "Find the Present": False}


def reset_game():
    st.session_state.stage = "welcome"
    st.session_state.ornaments = {"red": False, "blue": False, "gold": False}
    st.session_state.caught_count = 0
    st.session_state.find_choice = None
    st.session_state.missions_completed = {"Decorate the Tree": False, "Catch Snowflakes": False, "Find the Present": False}


# Small friendly helper for kid feedback
def kid_msg(text, emoji="✨"):
    return f"<div style='font-size:1.4rem;text-align:center;margin:8px 0 10px 0;color:#2b2b2b'>{emoji} <b>{text}</b></div>"

# --------------------------
# Header / Title
# --------------------------
st.markdown(f"<div class='title'>Rowan's Christmas Adventure</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>Let's help Rowan celebrate! 🎄 Click the big buttons — it's easy and fun.</div>", unsafe_allow_html=True)

# --------------------------
# Layout
# --------------------------
left_col, right_col = st.columns([3, 1], gap="medium")

with left_col:
    st.markdown("<div class='left'>", unsafe_allow_html=True)

    # Snowflakes floating across the left area (random positions & speeds)
    snow_html = "<div style='position:absolute;inset:0;overflow:hidden;'>"
    for i in range(8):
        left_pos = random.randint(2, 90)
        delay = random.uniform(0, 4)
        dur = random.uniform(6, 14)
        size = random.choice(["1.2rem", "1.6rem", "2rem", "2.4rem"])
        snow_html += f"<div class='snowflake' style='left:{left_pos}%; animation-duration:{dur}s; top:-5%; font-size:{size}; animation-delay:{delay}s'>❄️</div>"
    snow_html += "</div>"
    st.markdown(snow_html, unsafe_allow_html=True)

    # show content depending on stage
    if st.session_state.stage == "welcome":
        # Large start button
        st.markdown("<div style='text-align:center;margin-top:1.6rem'>", unsafe_allow_html=True)
        start_clicked = st.button("Start the Adventure! 🎅", key="start", help="Press to begin", on_click=None)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Hi Rowan! Let's play three easy missions.", "🎁"), unsafe_allow_html=True)
        st.markdown("<div class='hint'>Missions are big and simple: <br>Decorate, Catch Snowflakes, Find the Present</div>", unsafe_allow_html=True)
        if start_clicked:
            st.session_state.stage = "game"
            st.experimental_rerun()

    elif st.session_state.stage == "game":
        # Big friendly mission selection with animated mission effects
        st.markdown("<div style='display:flex;gap:18px;flex-wrap:wrap;justify-content:center;margin-top:6px'>", unsafe_allow_html=True)

        # Button: Decorate the Tree
        decorate_text = "Decorate the Tree 🌟"
        decorate_disabled = st.session_state.missions_completed["Decorate the Tree"]
        decorate_btn = st.button(decorate_text, key="decorate",
                                 help="Add three ornaments to the tree", disabled=decorate_disabled)
        # Button: Catch Snowflakes
        catch_text = "Catch Snowflakes ❄️"
        catch_disabled = st.session_state.missions_completed["Catch Snowflakes"]
        catch_btn = st.button(catch_text, key="catch", help="Catch 3 snowflakes", disabled=catch_disabled)
        # Button: Find the Present
        find_text = "Find the Present 🎁"
        find_disabled = st.session_state.missions_completed["Find the Present"]
        find_btn = st.button(find_text, key="find", help="Pick the right present", disabled=find_disabled)

        st.markdown("</div>", unsafe_allow_html=True)

        # Start the sub-stage depending on which mission clicked
        if decorate_btn:
            st.session_state.stage = "decorate"
            st.experimental_rerun()
        if catch_btn:
            st.session_state.stage = "catch"
            st.experimental_rerun()
        if find_btn:
            st.session_state.stage = "find"
            st.experimental_rerun()

        # Show progress
        completed = sum(1 for v in st.session_state.missions_completed.values() if v)
        st.markdown(f"<div style='text-align:center;margin-top:18px;font-size:1.25rem'>Missions completed: {completed} / 3</div>", unsafe_allow_html=True)

    elif st.session_state.stage == "decorate":
        st.markdown("<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:10px'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:2.4rem'>🌲 Decorate the tree</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Click an ornament to put it on the tree!", "🖐️"), unsafe_allow_html=True)

        # Draw tree (simple emoji tree) + ornaments placed
        tree_visual = "<div style='text-align:center;margin-top:12px'>"
        # create simple tree ascii with emoji spots where ornaments go
        # We'll show three spots: left, middle, right
        left_spot = "🔴" if st.session_state.ornaments["red"] else "⚪"
        mid_spot = "🔵" if st.session_state.ornaments["blue"] else "⚪"
        right_spot = "🟡" if st.session_state.ornaments["gold"] else "⚪"

        tree_visual += "<div style='font-size:5.2rem;line-height:0.8'>"
        tree_visual += "      🌲<br>"
        tree_visual += f"    {left_spot}  {mid_spot}  {right_spot}<br>"
        tree_visual += "      ⭐"
        tree_visual += "</div></div>"
        st.markdown(tree_visual, unsafe_allow_html=True)

        # Ornament selection area
        st.markdown("<div style='display:flex;gap:18px;justify-content:center;margin-top:18px'>", unsafe_allow_html=True)
        if not st.session_state.ornaments["red"]:
            if st.button("Put the red ornament 🔴", key="orn_red"):
                st.session_state.ornaments["red"] = True
        else:
            st.markdown("<div style='padding:12px;border-radius:14px;background:transparent;font-size:1.2rem'>Red ✔️</div>", unsafe_allow_html=True)

        if not st.session_state.ornaments["blue"]:
            if st.button("Put the blue ornament 🔵", key="orn_blue"):
                st.session_state.ornaments["blue"] = True
        else:
            st.markdown("<div style='padding:12px;border-radius:14px;background:transparent;font-size:1.2rem'>Blue ✔️</div>", unsafe_allow_html=True)

        if not st.session_state.ornaments["gold"]:
            if st.button("Put the gold ornament 🟡", key="orn_gold"):
                st.session_state.ornaments["gold"] = True
        else:
            st.markdown("<div style='padding:12px;border-radius:14px;background:transparent;font-size:1.2rem'>Gold ✔️</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Check if all are placed
        if all(st.session_state.ornaments.values()):
            # mark completed and give celebration
            st.session_state.missions_completed["Decorate the Tree"] = True
            st.markdown(kid_msg("The tree looks beautiful! Great job, Rowan! 🎉", "🎄"), unsafe_allow_html=True)
            if st.button("Back to Missions"):
                st.session_state.stage = "game"
                st.experimental_rerun()

        # Allow returning
        if st.button("Back", key="back_from_decorate"):
            st.session_state.stage = "game"
            st.experimental_rerun()

    elif st.session_state.stage == "catch":
        st.markdown("<div style='text-align:center;margin-top:4rem'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:2.6rem'>❄️ Catch Snowflakes</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Click the BIG catch button when you see snowflakes! Catch 3 to win.", "👀"), unsafe_allow_html=True)

        # Show animated falling snow area (passive visual)
        st.markdown("""
            <div style='width:520px;height:300px;border-radius:18px;margin:12px auto;display:flex;align-items:center;justify-content:center;position:relative;'>
              <div style='font-size:5rem'>☃️</div>
            </div>
        """, unsafe_allow_html=True)

        # Big catch button
        catch_clicked = st.button("CATCH! ❄️", key="catch_big")
        if catch_clicked:
            # success chance high for a 4-year-old to keep it fun
            # small random to make it feel interactive
            got = random.random() < 0.9
            if got:
                st.session_state.caught_count += 1
                st.success(f"Nice! You caught a snowflake. ❄️ Total: {st.session_state.caught_count}/3")
            else:
                st.info("Oh no, it slipped! Try again — you can do it!")

            # small pause to let celebration show
            time.sleep(0.2)

        st.markdown(f"<div style='text-align:center;margin-top:12px;font-size:1.25rem'>Snowflakes caught: <b>{st.session_state.caught_count}</b> / 3</div>", unsafe_allow_html=True)

        if st.session_state.caught_count >= 3:
            st.session_state.missions_completed["Catch Snowflakes"] = True
            st.balloons()
            st.markdown(kid_msg("Amazing! You caught 3 snowflakes! 🎉", "❄️"), unsafe_allow_html=True)
            if st.button("Back to Missions"):
                st.session_state.stage = "game"
                st.experimental_rerun()

        if st.button("Back", key="back_from_catch"):
            st.session_state.stage = "game"
            st.experimental_rerun()

    elif st.session_state.stage == "find":
        st.markdown("<div style='text-align:center;margin-top:2rem'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:2.4rem'>🎁 Find the Present</div>", unsafe_allow_html=True)
        st.markdown(kid_msg("Pick a present. One has a surprise! Try one.", "🔍"), unsafe_allow_html=True)

        # Show three presents
        st.markdown("<div style='display:flex;justify-content:center;gap:26px;margin-top:18px'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        presents = ["🎁", "🎀", "🧸"]
        # hidden correct present
        if st.session_state.find_choice is None:
            correct = random.choice([1, 2, 3])
            st.session_state._correct_present = correct
        else:
            correct = st.session_state._correct_present

        with col1:
            if st.button(presents[0], key="present1"):
                st.session_state.find_choice = 1
        with col2:
            if st.button(presents[1], key="present2"):
                st.session_state.find_choice = 2
        with col3:
            if st.button(presents[2], key="present3"):
                st.session_state.find_choice = 3
        st.markdown("</div>", unsafe_allow_html=True)

        # If a choice was made, reveal
        if st.session_state.find_choice is not None:
            choice = st.session_state.find_choice
            if choice == correct:
                st.session_state.missions_completed["Find the Present"] = True
                st.balloons()
                st.markdown(kid_msg("You found the surprise! Yay!! 🎉", "✨"), unsafe_allow_html=True)
                st.markdown("<div style='text-align:center;margin-top:10px;font-size:1.6rem'>You found a cuddly bear 🧸 and a sticker!</div>", unsafe_allow_html=True)
                if st.button("Back to Missions"):
                    st.session_state.stage = "game"
                    st.experimental_rerun()
            else:
                st.markdown(kid_msg("Ooops — not that one. Try another!", "😅"), unsafe_allow_html=True)
                if st.button("Try again"):
                    st.session_state.find_choice = None
                    st.experimental_rerun()
                if st.button("Back"):
                    st.session_state.stage = "game"
                    st.experimental_rerun()

        if st.button("Back to Missions", key="back_from_find"):
            st.session_state.stage = "game"
            st.experimental_rerun()

    elif st.session_state.stage == "finished":
        # Celebration screen (should rarely be directly landed on)
        st.markdown("<div style='text-align:center;margin-top:3rem'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:3.2rem'>🎉 All Missions Done!</div>", unsafe_allow_html=True)
        st.balloons()
        st.markdown(kid_msg("Great job, Rowan! Merry Christmas! 🎄", "🎅"), unsafe_allow_html=True)
        if st.button("Play again"):
            reset_game()
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Missions sidebar (shows completion, animated for active mission)
    st.markdown("<div class='right'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.6rem;margin-bottom:6px'>Missions</div>", unsafe_allow_html=True)

    # Display missions with pulse for the next incomplete one
    for name, done in st.session_state.missions_completed.items():
        cls = "mission"
        if not done and not any(not v for v in list(st.session_state.missions_completed.values())[:list(st.session_state.missions_completed.keys()).index(name)]):
            # this logic attempts to pulse the first incomplete in order
            cls += " pulse"
        if done:
            st.markdown(f"<div class='{cls}'><span style='font-size:1.2rem'>{name}</span><span style='font-size:1.1rem'>✅</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='{cls}'><span style='font-size:1.2rem'>{name}</span><span style='font-size:1.1rem'>•</span></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px;font-size:1.05rem;color:#2b2b2b'>Finished missions will show a check. When all three are done, a big surprise awaits!</div>", unsafe_allow_html=True)

    # If all done, show big celebration and reset option
    if all(st.session_state.missions_completed.values()):
        st.markdown("<div style='margin-top:12px;text-align:center'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:1.8rem'>🎊 You finished them all!</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:1.05rem;margin-top:8px'>Press the button to see a celebration for Rowan.</div>", unsafe_allow_html=True)
        if st.button("Celebrate! 🎉"):
            # show confetti block (CSS animated)
            confetti_html = "<div class='confetti'>"
            colors = ["💚","💚","❤️","💛","💙","💜","💚"]
            for i in range(24):
                left = random.randint(2, 95)
                top = random.randint(-30, 0)
                dur = random.uniform(3, 9)
                size = random.choice(["1.2rem", "1.6rem", "2rem", "2.6rem"])
                emoji = random.choice(colors)
                confetti_html += f"<i style='left:{left}%;top:{top}vh;font-size:{size};animation-duration:{dur}s'>{emoji}</i>"
            confetti_html += "</div>"
            st.markdown(confetti_html, unsafe_allow_html=True)
            st.session_state.stage = "finished"
            st.experimental_rerun()

    # Small credits and reset
    st.markdown("<div style='margin-top:16px;text-align:center'>Made with ❤️ for Rowan. Big letters, bright colors — perfect for little hands.</div>", unsafe_allow_html=True)
    if st.button("Reset Game (start over)"):
        reset_game()
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# End of app
# --------------------------
