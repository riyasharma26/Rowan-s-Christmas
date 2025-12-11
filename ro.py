import streamlit as st
import time
import random

# -----------------------------
# UPDATED APP WITH CHRISTMAS BACKGROUND & SECOND MISSION
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Rowan's Christmas Adventure", layout="centered")

# -----------------------------
# STYLE – CHRISTMAS COLORS & FUN
# -----------------------------
st.markdown(
    """
    <style>
        body {background: linear-gradient(135deg, #0a5a0a, #b30000);}
        .title-bubble {
            background: linear-gradient(135deg, #ff2e2e, #1fa30a);
            padding: 25px 40px;
            border-radius: 50px;
            color: white;
            font-size: 40px;
            text-align: center;
            font-weight: 800;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .mission-box {
            background: white;
            border: 5px solid #ff2e2e;
            padding: 20px;
            border-radius: 25px;
            box-shadow: 0 0 15px rgba(0,0,0,0.15);
            text-align: center;
        }
        .stickboy {
            font-size: 70px;
            text-align: center;
        }
        .certificate {
            border: 8px solid #1fa30a;
            border-radius: 20px;
            padding: 30px;
            background: #fff;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<div class='title-bubble'>ROWAN'S CHRISTMAS ADVENTURE 🎄✨</div>", unsafe_allow_html=True)

# -----------------------------
# MISSION 1 — WALKING ANIMATION
# -----------------------------
st.markdown("<div class='mission-box'><h2>Mission 1: Help Rowan Deliver the Christmas Present! 🎁</h2></div>", unsafe_allow_html=True)

st.write("\n")

frames = ["(ʘ‿ʘ)  🚶", "(•‿•)  🚶‍♂️", "(ᵔ◡ᵔ)  🚗💨", "(ᵔ◡ᵔ)  🚗💨💨"]

if "animate" not in st.session_state:
    st.session_state.animate = False
if "mission1_done" not in st.session_state:
    st.session_state.mission1_done = False
if "mission2_done" not in st.session_state:
    st.session_state.mission2_done = False

placeholder = st.empty()

if st.button("Start Mission 1!") and not st.session_state.mission1_done:
    st.session_state.animate = True

if st.session_state.animate and not st.session_state.mission1_done:
    for i in range(20):
        placeholder.markdown(f"<div class='stickboy'>{random.choice(frames)}</div>", unsafe_allow_html=True)
        time.sleep(0.15)
    placeholder.empty()
    st.session_state.animate = False
    st.session_state.mission1_done = True
    st.success("Mission 1 Complete! 🎉")

# -----------------------------
# MISSION 2 — FIND THE PRESENT GAME
# -----------------------------
st.markdown("<div class='mission-box'><h2>Mission 2: Find the Hidden Christmas Present! 🎄🎁</h2></div>", unsafe_allow_html=True)

if st.session_state.mission1_done:
    st.write("Three boxes appear. One has the present. Pick the right one!")
    boxes = ["📦", "📦", "📦"]
    present_index = random.randint(0, 2)

    choice = st.radio("Which box has the present?", [1, 2, 3])

    if st.button("Check Box"):
        if choice - 1 == present_index:
            st.success("You found the present! 🎁✨ Mission 2 Complete!")
            st.session_state.mission2_done = True
        else:
            st.error("Not here! Try again! ❌")
else:
    st.info("Complete Mission 1 first!")

# -----------------------------
# CERTIFICATE
# -----------------------------
if st.session_state.mission1_done and st.session_state.mission2_done:
    st.markdown(
        """
        <div class='certificate'>
            <h1>🎉 Certificate of Christmas Bravery 🎉</h1>
            <h2>This certifies that <b>Rowan</b></h2>
            <h3>completed ALL Christmas Adventure Missions!</h3>
            <p>You delivered the present AND found the hidden gift. Amazing job, hero! 🎁🎄✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("<div class='mission-box'><h2>Mission: Help Rowan Deliver the Christmas Present! 🎁</h2></div>", unsafe_allow_html=True)

st.write("\n")

# Stick figure frames (simple animation)
frames = [
    "(ʘ‿ʘ)  🚶",  # walking 1
    "(•‿•)  🚶‍♂️", # walking 2
    "(ᵔ◡ᵔ)  🚗💨", # driving 1
    "(ᵔ◡ᵔ)  🚗💨💨", # driving 2
]

if "animate" not in st.session_state:
    st.session_state.animate = False
if "won" not in st.session_state:
    st.session_state.won = False

placeholder = st.empty()

# Animation button
if st.button("Start Mission!"):
    st.session_state.animate = True

# Run animation
if st.session_state.animate and not st.session_state.won:
    for i in range(20):
        frame = random.choice(frames)
        placeholder.markdown(f"<div class='stickboy'>{frame}</div>", unsafe_allow_html=True)
        time.sleep(0.15)
    st.session_state.animate = False
    st.session_state.won = True
    placeholder.empty()

# -----------------------------
# CERTIFICATE WHEN HE WINS
# -----------------------------
if st.session_state.won:
    st.markdown(
        """
        <div class='certificate'>
            <h1>🎉 Certificate of Christmas Bravery 🎉</h1>
            <h2>This certifies that <b>Rowan</b></h2>
            <h3>successfully completed his Christmas Adventure!</h3>
            <p>He delivered the present and saved Christmas! 🎁🎄</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
