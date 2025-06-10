# ai_content_generator_app.py

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env or environment variable
load_dotenv()
GENAI_API_KEY = os.getenv("AIzaSyAGK2xPMFId5G6k6BXMz18B_Ro1-DgW2_k")

# Configure Gemini API
genai.configure(api_key="AIzaSyAGK2xPMFId5G6k6BXMz18B_Ro1-DgW2_k")
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="📝",
    layout="wide"
)

# App Title
st.title("📝 AI Content Generator")
st.markdown(
    """
    Generate professional content for **blogs**, **marketing**, **emails**, and more  
    using the power of **Google Gemini LLM** ✨
    """
)

# Sidebar
st.sidebar.header("🛠️ Settings")
content_type = st.sidebar.selectbox(
    "Content Type",
    ["Blog Post", "Marketing Copy", "Email", "Social Media Caption", "Product Description"]
)

tone = st.sidebar.selectbox(
    "Tone of Voice",
    ["Professional", "Friendly", "Persuasive", "Informative", "Casual", "Luxury"]
)

length = st.sidebar.slider(
    "Content Length (words approx.)",
    min_value=50,
    max_value=1000,
    step=50,
    value=300
)

# Main Input
prompt = st.text_area(
    "✍️ Enter your content topic / idea / instructions:",
    placeholder="e.g. How AI is transforming digital marketing"
)

# Generate button
if st.button("🚀 Generate Content"):
    if not prompt.strip():
        st.warning("Please enter a prompt/topic first.")
    else:
        with st.spinner("Generating content... ⏳"):
            full_prompt = f"""
            Generate a {length}-word {content_type.lower()}.
            Tone of voice: {tone}.
            Topic/Instructions: {prompt}.
            """
            try:
                response = model.generate_content(full_prompt)
                generated_text = response.text.strip()
                st.success("✅ Content Generated!")
                st.markdown("### ✨ Generated Content")
                st.write(generated_text)

                # Option to download
                st.download_button(
                    label="📥 Download as .txt",
                    data=generated_text,
                    file_name=f"{content_type.replace(' ', '_')}.txt",
                    mime="text/plain"
                )

                # Save to session history
                if 'history' not in st.session_state:
                    st.session_state['history'] = []
                st.session_state['history'].append((prompt, generated_text))

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display previous responses
if 'history' in st.session_state and st.session_state['history']:
    with st.expander("📜 View Previous Generations"):
        for idx, (prev_prompt, prev_response) in enumerate(st.session_state['history'][::-1]):
            st.markdown(f"**Prompt {len(st.session_state['history'])-idx}:** {prev_prompt}")
            st.write(prev_response)
            st.markdown("---")
