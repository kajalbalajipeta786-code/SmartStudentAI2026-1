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

import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Clear chat"):
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
                reply = client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=1000,
                    system=SYSTEM_PROMPT,
                    messages=st.session_state.history,
                )
           response = model.generate_content(prompt)
text = response.text
