import logging
import queue
import time

import streamlit as st
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

logger = logging.getLogger(__name__)

st.title("WebRTC Colornamer")
image_placeholder = st.empty()

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

""" Simple video loopback """
webrtc_ctx = webrtc_streamer(
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
            logger.warning(" Queue is empty. Abort.")
            break

        img_rgb = video_frame.to_ndarray(format="rgb24")
        image_placeholder.image(img_rgb)
        logger.info("Displayed a frame, let's sleep for a second.")
        time.sleep(1)
    else:
        logger.warning("AudioReciver is not set. Abort.")
        break