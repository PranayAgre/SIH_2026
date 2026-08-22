import streamlit as st
import time

# --- PAGE CONFIGURATION (Accessibility First) ---
st.set_page_config(
    page_title="Elderly Assistance Portal",
    page_icon="👵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ACCESSIBILITY CSS STYLING ---
st.markdown("""
    <style>
    /* High contrast background & large default font */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Large high-contrast action buttons */
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 26px !important;
        font-weight: bold !important;
        border-radius: 16px !important;
        border: 3px solid #1D3557 !important;
        background-color: #1D3557 !important;
        color: white !important;
        margin-bottom: 15px;
    }
    
    div.stButton > button:hover {
        background-color: #457B9D !important;
        border-color: #457B9D !important;
        color: white !important;
    }

    /* Custom Cards for Reminders & Games */
    .patient-card {
        background-color: #FFFFFF;
        border: 3px solid #2A9D8F;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
    }

    .card-title {
        font-size: 30px;
        font-weight: 800;
        color: #264653;
        margin-bottom: 10px;
    }

    .card-text {
        font-size: 22px;
        color: #2B2D42;
    }
    </style>
""", unsafe_allow_html=True)

# --- BROWSER TEXT-TO-SPEECH (AUDIO GUIDANCE) ---
def speak(text):
    """Executes browser-native JavaScript to speak text out loud."""
    js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.rate = 0.85; // Slower rate for elderly listeners
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# --- NAVIGATION HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 44px; color: #1D3557;'>👵 Good Morning! Welcome Home</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px; color: #457B9D;'>Tap any big button below to begin</p>", unsafe_allow_html=True)

st.divider()

# --- TOP NAVIGATION BUTTONS ---
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    if st.button("🧩 Memory Game", key="nav_game"):
        st.session_state['active_tab'] = "game"
        speak("Opening cognitive memory game")

with col_nav2:
    if st.button("💊 Daily Schedule", key="nav_schedule"):
        st.session_state['active_tab'] = "schedule"
        speak("Opening daily schedule and medication reminders")

# Default active tab setup
if 'active_tab' not in st.session_state or st.session_state['active_tab'] == "photos":
    st.session_state['active_tab'] = "game"

st.write("<br>", unsafe_allow_html=True)

# ==========================================
# MODULE 1: COGNITIVE COLOR PATTERN GAME
# ==========================================
if st.session_state['active_tab'] == "game":
    st.markdown("<div class='patient-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🧩 Color Memory Game</div>", unsafe_allow_html=True)
    st.markdown("<div class='card-text'>Look at the target color and tap the matching button!</div><br>", unsafe_allow_html=True)

    # Initialize Game State
    if 'target_color' not in st.session_state:
        st.session_state['target_color'] = "RED"
        st.session_state['score'] = 0

    st.markdown(f"<h2 style='font-size: 32px;'>Target Color: <span style='color:#E63946;'>{st.session_state['target_color']}</span></h2>", unsafe_allow_html=True)

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        if st.button("🔴 RED", key="btn_red"):
            if st.session_state['target_color'] == "RED":
                st.session_state['score'] += 10
                speak("Correct! Great job.")
                st.balloons()
                st.session_state['target_color'] = "BLUE"
            else:
                speak("Try again!")

    with col_g2:
        if st.button("🔵 BLUE", key="btn_blue"):
            if st.session_state['target_color'] == "BLUE":
                st.session_state['score'] += 10
                speak("Wonderful! You matched the blue color.")
                st.balloons()
                st.session_state['target_color'] = "GREEN"
            else:
                speak("Try again!")

    with col_g3:
        if st.button("🟢 GREEN", key="btn_green"):
            if st.session_state['target_color'] == "GREEN":
                st.session_state['score'] += 10
                speak("Excellent work!")
                st.balloons()
                st.session_state['target_color'] = "RED"
            else:
                speak("Try again!")

    st.markdown(f"<br><h3 style='font-size: 28px; color: #2A9D8F;'>Total Stars Earned: ⭐ {st.session_state['score']} Points</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE 2: DAILY SCHEDULE & REMINDERS
# ==========================================
elif st.session_state['active_tab'] == "schedule":
    st.markdown("<div class='patient-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>💊 Today's Routine</div>", unsafe_allow_html=True)
    
    # Task 1
    st.markdown("<p class='card-text'><b>1. Morning Medicine (8:30 AM)</b></p>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("🔊 Listen to Reminder", key="rem1"):
            speak("Time to take 1 red pill after breakfast.")
    with c2:
        if st.button("✅ Done", key="done1"):
            speak("Medicine marked as taken.")
            st.success("Completed!")

    st.divider()

    # Task 2
    st.markdown("<p class='card-text'><b>2. Drink Water (11:00 AM)</b></p>", unsafe_allow_html=True)
    c3, c4 = st.columns([2, 1])
    with c3:
        if st.button("🔊 Listen to Reminder", key="rem2"):
            speak("Please drink one full glass of water.")
    with c4:
        if st.button("✅ Done", key="done2"):
            speak("Water break marked as completed.")
            st.success("Completed!")

    st.markdown("</div>", unsafe_allow_html=True)