import streamlit as st
from openai import OpenAI

# Set up the Web Page Layout
st.set_page_config(page_title="TTS Language Suite", page_icon="🌐")
st.title("🌐 Multilingual Text-to-Speech Platform")
st.write("Select a language, input your script, and generate an MP3 file instantly.")

# Your secure key built into the platform
MY_SECRET_KEY = "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"
client = OpenAI(api_key=MY_SECRET_KEY)

# 1. Dropdown Menu for Target Languages
language_options = [
    "Dutch (nl_NL)",
    "French (fr_FR)",
    "Spanish (es_ES)",
    "German (de_DE)",
    "English (en_US)",
    "English (en_GB)",
    "Italian (it_IT)"
]
selected_language = st.selectbox("Select Target Language/Dialect:", language_options)

# 2. Sidebar Option to Choose the Voice Persona
voice_choice = st.sidebar.selectbox("Select Voice Persona:", ["coral", "alloy", "echo", "fable", "onyx", "nova", "shimmer"])

# 3. Input Box for your Script
script_input = st.text_area(
    label=f"Input Script for {selected_language}:", 
    placeholder="Type or paste your 5-10 word cultural phrase here..."
)

# 4. Action Button to process and output the MP3
if st.button("Generate MP3 Audio"):
    if not script_input.strip():
        st.warning("Please type a script into the input box first!")
    else:
        with st.spinner("Generating authentic audio from OpenAI..."):
            try:
                # Request speech from OpenAI's neural engine
                response = client.audio.speech.create(
                    model="gpt-4o-mini-tts",
                    voice=voice_choice,
                    input=script_input
                )
                
                # Fetch the raw audio stream data
                audio_bytes = response.read()
                
                st.write("---")
                st.subheader("🎵 Generated Output")
                
                # Render a live audio playback widget right in the browser
                st.audio(audio_bytes, format="audio/mp3")
                
                # Create a clean downloadable MP3 button link
                clean_lang_name = selected_language.lower().split(" ")[0]
                st.download_button(
                    label="📥 Download MP3 File",
                    data=audio_bytes,
                    file_name=f"{clean_lang_name}_audio.mp3",
                    mime="audio/mp3"
                )
                st.success("MP3 generated successfully!")
                
            except Exception as e:
                st.error(f"An error occurred while connecting to OpenAI: {e}")
