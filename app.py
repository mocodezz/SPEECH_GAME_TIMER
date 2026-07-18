from streamlit_webrtc import webrtc_streamer
import av
import time
import streamlit as st
import random

st.set_page_config(page_title="Speak on a Topic", page_icon="🎤", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #ff512f, #dd2476, #1fa2ff, #12d8fa);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
h1 { font-size: 4rem !important; }
h2 { font-size: 3rem !important; }
</style>
""", unsafe_allow_html=True)

topics = ["Climate change", "AI ethics", "Space exploration", "Minimum wage", "Social media addiction"]
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None
if "running" not in st.session_state:
    st.session_state.running = False

st.title("Speak on a Topic")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = img[:, ::-1, :]
    return av.VideoFrame.from_ndarray(img, format="bgr24")

if st.button("Give me a topic"):
    st.session_state.running = True

if st.session_state.running:
    camera_placeholder = st.empty()
    with camera_placeholder.container():
        webrtc_streamer(
            key="mirror",
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False},
        )

    choice = random.choice(topics)
    while choice == st.session_state.last_topic:
        choice = random.choice(topics)
    st.session_state.last_topic = choice

    topic_placeholder = st.empty()
    delay = 0.04
    for i in range(20):
        topic_placeholder.subheader(random.choice(topics))
        time.sleep(delay)
        delay += 0.015
    topic_placeholder.subheader(choice)

    st.toast("Heres your Topic")
    timer_placeholder = st.empty()
    for seconds_left in range(60, 0, -1):
        timer_placeholder.metric("Time left", f"{seconds_left}s")
        time.sleep(1)
    timer_placeholder.error("Time's up!")

    camera_placeholder.empty()
    st.session_state.running = False