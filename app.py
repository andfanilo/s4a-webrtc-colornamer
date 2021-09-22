import streamlit as st
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

st.title("WebRTC Colornamer")
image_placeholder = st.empty()

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

""" Simple video loopback """
webrtc_streamer(
    key="video-colornamer",
    mode=WebRtcMode.SENDONLY,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True},
)

while True:
    if webrtc_ctx.video_receiver:
        try:
            video_frame = webrtc_ctx.video_receiver.get_frame(timeout=1)
        except queue.Empty:
            print("Queue is empty. Abort.")
            break

        img_rgb = video_frame.to_ndarray(format="rgb24")
        image_placeholder.image(img_rgb)
    else:
        print("AudioReciver is not set. Abort.")
        break