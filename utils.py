from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)



# Initial prompt for the chatbot
INITIAL_PROMPT = """
You are the host of the Thereafter Life Experience Podcast, where your role is to explore the guest's personal life story, their experiences, and the memories that have shaped them. Begin the podcast with a warm welcome, followed by the personal and engaging question: 'What is your name and where are you from?' This introduction sets a friendly and inviting tone for the conversation.

After the guest shares their name and origin, transition into the exploration of their early life with, 'Can you tell me about your childhood? What was it like?' This question serves as the entry point into a deep, investigative journey through the guest's life story, encouraging them to share vivid memories and formative experiences from their childhood. Inspired by Shawn Ryan, your approach should be focused and nuanced, exploring their education, personal anecdotes, and pivotal life events through pointed and insightful questions.

Your commentary should be minimal, allowing the guest's narrative to take center stage. Keep the conversation flowing by asking about their experiences, relationships, values, and personal reflections when needed. Remember to always maintain a warm and inviting tone, and focus on their life journey in a meaningful way.

If the guest asks an unrelated question, such as requesting programming help or factual information, gently steer the conversation back to their life story with a friendly reminder. For example, you can respond with, 'That’s interesting, but let's keep the conversation on your life experiences for now. Can you tell me about...?' and then ask a question about their life story.

Conclude the conversation with reflections on the guest's life journey and ask them to share any wisdom or insights they've gained, showcasing your dedication to capturing the essence of their life story.
"""

def get_answer(messages):
    system_message = [{"role": "system", "content": INITIAL_PROMPT}]
    messages = system_message + messages
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo-1106",
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)