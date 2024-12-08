# import streamlit as st
# import os
# from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
# from audio_recorder_streamlit import audio_recorder
# from streamlit_float import *

# # Float feature initialization
# float_init()

# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "Hi! How are you? You can begin by clicking on the record button."}
#         ]
#     # if "audio_initialized" not in st.session_state:
#     #     st.session_state.audio_initialized = False

# initialize_session_state()

# st.title("Thereafter Life Experience Podcast 🎙️")

# # Create footer container for the microphone
# footer_container = st.container()
# with footer_container:
#     audio_bytes = audio_recorder()

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# if audio_bytes:
#     # Write the audio bytes to a file
#     with st.spinner("Transcribing..."):
#         webm_file_path = "temp_audio.mp3"
#         with open(webm_file_path, "wb") as f:
#             f.write(audio_bytes)

#         transcript = speech_to_text(webm_file_path)
#         if transcript:
#             st.session_state.messages.append({"role": "user", "content": transcript})
#             with st.chat_message("user"):
#                 st.write(transcript)
#             os.remove(webm_file_path)

# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking🤔..."):
#             final_response = get_answer(st.session_state.messages)
#         with st.spinner("Generating audio response..."):    
#             audio_file = text_to_speech(final_response)
#             autoplay_audio(audio_file)
#         st.write(final_response)
#         st.session_state.messages.append({"role": "assistant", "content": final_response})
#         os.remove(audio_file)

# # Float the footer container and provide CSS to target it with
# footer_container.float("bottom: 0rem;")

import streamlit as st
import os
import tempfile
from utils import get_answer, text_to_speech, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How are you? You can begin by clicking on the record button."}
        ]

initialize_session_state()

st.title("Thereafter Life Experience Podcast 🎙️")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    # Write the audio bytes to a temporary file
    with st.spinner("Transcribing..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Transcribe the audio
        transcript = speech_to_text(temp_audio_path)
        os.remove(temp_audio_path)  # Clean up the temporary file

        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)

        with st.spinner("Generating audio response..."):
            # Generate audio response
            audio_file = text_to_speech(final_response)

            # Convert the audio file into a base64 string for autoplay
            import base64
            audio_bytes = open(audio_file, "rb").read()
            audio_base64 = base64.b64encode(audio_bytes).decode()

            # Use HTML with autoplay to play audio
            audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})

        os.remove(audio_file)  # Clean up the temporary audio file

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")
