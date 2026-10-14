import streamlit as st
import anthropic

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.history:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Ask me anything"):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    reply = client.messages.create(
        model="claude-sonnet-5", max_tokens=1000,
        system="You are a helpful assistant.",
        messages=st.session_state.history,
    )
    text = reply.content[0].text
    st.session_state.history.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)
