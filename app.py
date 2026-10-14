import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Smart Student AI", page_icon="🎓")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Add GEMINI_API_KEY in Settings → Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
SYSTEM_PROMPT = (
    "You are Smart Student AI, a friendly study assistant. "
    "Explain things simply, give examples, and help with homework, "
    "writing, and exam prep. If you are unsure, say so."
)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Add GEMINI_API_KEY in Settings → Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Clear chat"):
    st.session_state.history = []
    st.rerun()

if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button(
    "🗑️ Clear Chat",
    key="clear_chat_btn"
):
    st.session_state.history = []
    st.rerun()

for m in st.session_state.history:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Ask me anything"):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)
                text = response.text

        except Exception as e:
            text = f"Error: {e}"

        st.write(text)

    st.session_state.history.append({"role": "assistant", "content": text})
