import streamlit as st
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

st.title("WebRTC Colornamer")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

""" Simple video loopback """
webrtc_streamer(
    key="loopback",
    rtc_configuration=RTC_CONFIGURATION,
)