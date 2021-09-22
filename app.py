import logging
import queue
import time

import numpy as np
from colornamer import get_color_from_rgb
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
text_placeholder = st.empty()

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
    logger.debug("Entering infinite loop.")
    if webrtc_ctx.video_receiver:
        try:
            video_frame = webrtc_ctx.video_receiver.get_frame(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        img_rgb = video_frame.to_ndarray(format="rgb24")
        image_placeholder.image(img_rgb)
        
        avg_color_per_row = np.average(np_img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        color_names = get_color_from_rgb(avg_color)
        text_placeholder.markdown(f"The Common Color in selected zone is: {color_names['common_color']}")

        logger.info("Displayed a frame, let's sleep for a second.")
        time.sleep(1)
    else:
        logger.warning("AudioReciver is not set. Abort.")
        break