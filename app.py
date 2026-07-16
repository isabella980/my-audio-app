import streamlit as st
from openai import OpenAI

# Set up the Web Page Layout
st.set_page_config(page_title="Global TTS Suite", page_icon="🌐")
st.title("🌐 Global Multilingual Text-to-Speech Platform")
st.write("Enter your credentials, choose from our expanded language catalog, and generate an MP3.")

# 1. Secure API Key Input Box in Sidebar (Stops GitHub from revoking keys)
st.sidebar.header("🔑 Authentication")
user_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", placeholder="sk-proj-...")

# 2. Vastly Expanded Dropdown Menu for Global Target Languages
language_options = [
    "Afrikaans (af_ZA)",
    "Arabic (ar_AE)",
    "Armenian (hy_AM)",
    "Azerbaijani (az_AZ)",
    "Belarusian (be_BY)",
    "Bosnian (bs_BA)",
    "Bulgarian (bg_BG)",
    "Catalan (ca_ES)",
    "Chinese, Mandarin (zh_CN)",
    "Croatian (hr_HR)",
    "Czech (cs_CZ)",
    "Danish (dk_DK)",
    "Dutch (nl_NL)",
    "English (en_US)",
    "English (en_GB)",
    "English (en_AU)",
    "English (en_CA)",
    "English (en_IN)",
    "Estonian (et_EE)",
    "Finnish (fi_FI)",
    "French (fr_FR)",
    "French (fr_CA)",
    "Galician (gl_ES)",
    "German (de_DE)",
    "Greek (el_GR)",
    "Hebrew (he_IL)",
    "Hindi (hi_IN)",
    "Hungarian (hu_HU)",
    "Icelandic (is_IS)",
    "Indonesian (id_ID)",
    "Italian (it_IT)",
    "Japanese (ja_JP)",
    "Kannada (kn_IN)",
    "Kazakh (kk_KZ)",
    "Korean (ko_KR)",
    "Latvian (lv_LV)",
    "Lithuanian (lt_LT)",
    "Macedonian (mk_MK)",
    "Malay (ms_MY)",
    "Marathi (mr_IN)",
    "Māori (mi_NZ)",
    "Nepali (ne_NP)",
    "Norwegian (no_NO)",
    "Persian (fa_IR)",
    "Polish (pl_PL)",
    "Portuguese (pt_BR)",
    "Portuguese (pt_PT)",
    "Romanian (ro_RO)",
    "Russian (ru_RU)",
    "Serbian (sr_RS)",
    "Slovak (sk_SK)",
    "Slovenian (sl_SI)",
    "Spanish (es_ES)",
    "Spanish (es_MX)",
    "Swahili (sw_KE)",
    "Swedish (sv_SE)",
    "Tagalog/Filipino (tl_PH)",
    "Tamil (tm_IN)",
    "Thai (th_TH)",
    "Turkish (tr_TR)",
    "Ukrainian (uk_UA)",
    "Urdu (ur_PK)",
    "Vietnamese (vi_VN)",
    "Welsh (cy_GB)"
]
selected_language = st.selectbox("Select Target Language/Dialect:", language_options)

# 3. Sidebar Option to Choose the Voice Persona
voice_choice = st.sidebar.selectbox("Select Voice Persona:", ["coral", "alloy", "echo", "fable", "onyx", "nova", "shimmer"])

# 4. Input Box for your Script
script_input = st.text_area(
    label=f"Input Script for {selected_language}:", 
    placeholder="Type or paste your text content phrase here..."
)

# 5. Action Button to process and output the MP3
if st.button("Generate MP3 Audio"):
    if not user_api_key.strip():
        st.error("Please enter a valid OpenAI API key in the sidebar panel!")
    elif not script_input.strip():
        st.warning("Please type a script into the input box first!")
    else:
        with st.spinner("Generating authentic audio from OpenAI..."):
            try:
                # Initialize the OpenAI client using the user's input key
                client = OpenAI(api_key=user_api_key)
                
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
                clean_lang_name = selected_language.lower().split(" ")[0].replace(",", "")
                st.download_button(
                    label="📥 Download MP3 File",
                    data=audio_bytes,
                    file_name=f"{clean_lang_name}_audio.mp3",
                    mime="audio/mp3"
                )
                st.success("MP3 generated successfully!")
                
            except Exception as e:
                st.error(f"An error occurred while connecting to OpenAI: {e}")
