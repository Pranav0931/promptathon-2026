%%writefile app.py
import streamlit as st
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(
    page_title="Text Summariser",
    page_icon="✨",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Sora', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #f0f0f0;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            color: #e2c4ff;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #a89ec9;
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }

        .stTextArea textarea {
            background-color: #1e1b33;
            color: #f0f0f0;
            border: 1px solid #5a4fa0;
            border-radius: 10px;
            font-family: 'Sora', sans-serif;
            font-size: 0.9rem;
        }

        .stTextInput input {
            background-color: #1e1b33;
            color: #f0f0f0;
            border: 1px solid #5a4fa0;
            border-radius: 10px;
            font-family: 'Sora', sans-serif;
        }

        .stButton > button {
            background: linear-gradient(90deg, #7b5ea7, #a678d8);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 2rem;
            font-family: 'Sora', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #a678d8, #c9a8f5);
            transform: scale(1.02);
        }

        .summary-box {
            background-color: #1e1b33;
            border-left: 4px solid #a678d8;
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            color: #e8e0ff;
            font-size: 0.95rem;
            line-height: 1.7;
            margin-top: 1rem;
        }

        .word-count {
            color: #a89ec9;
            font-size: 0.8rem;
            margin-top: 0.4rem;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown("<h1>✨ Text Summariser</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Paste any text below and get a crisp summary powered by Gemini.</p>', unsafe_allow_html=True)

# --- API Key Input ---
api_key = st.text_input(
    "AIzaSyAa9d3byTRJsRV7JAeNq6ep4F5zwuKupUg",
    type="password",
    placeholder="AIzaSyAa9d3byTRJsRV7JAeNq6ep4F5zwuKupUg",
    help="Get your free key at https://aistudio.google.com/app/apikey"
)

# --- Text Input ---
user_text = st.text_area(
    "📄 Your Text",
    height=220,
    placeholder="Paste the text you want to summarise here...",
    label_visibility="visible"
)

# Word count display
if user_text.strip():
    word_count = len(user_text.split())
    st.markdown(f'<p class="word-count">{word_count} words</p>', unsafe_allow_html=True)

# --- Summarise Button ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    summarise_btn = st.button("Summarise ✦", use_container_width=True)

# --- Logic ---
if summarise_btn:
    if not api_key.strip():
        st.warning("⚠️ Please enter your Gemini API key.")
    elif not user_text.strip():
        st.warning("⚠️ Please paste some text to summarise.")
    elif len(user_text.split()) < 20:
        st.warning("⚠️ Please enter at least 20 words for a meaningful summary.")
    else:
        with st.spinner("Summarising with Gemini..."):
            try:
                genai.configure(api_key=api_key.strip())
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"""Summarise the following text clearly and concisely in 3–5 sentences.
Focus on the key points and main ideas. Write in plain English suitable for a general audience.

Text:
{user_text}

Summary:"""

                response = model.generate_content(prompt)
                summary = response.text.strip()

                st.markdown("### 📝 Summary")
                st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

                # Copy-friendly expander
                with st.expander("📋 Copy summary as plain text"):
                    st.code(summary, language=None)

            except Exception as e:
                error_msg = str(e)
                if "API_KEY" in error_msg.upper() or "invalid" in error_msg.lower():
                    st.error("❌ Invalid API key. Please double-check and try again.")
                elif "quota" in error_msg.lower():
                    st.error("❌ API quota exceeded. Try again later or check your Gemini plan.")
                else:
                    st.error(f"❌ Something went wrong: {error_msg}")

# --- Footer ---
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#6b6390; font-size:0.8rem;">Powered by Google Gemini · Built with Streamlit</p>',
    unsafe_allow_html=True
)
