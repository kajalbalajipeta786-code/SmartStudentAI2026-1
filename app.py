import streamlit as st

def generate_notes(topic):
    return f"""
# Study Notes: {topic}

These are sample notes for **{topic}**.
Replace this function with your AI code later.
"""

page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "📚 Notes", "❓ Quiz"]
)

if page == "🏠 Home":
    st.title("🏠 Home")
    st.write("Welcome to Smart Student AI")

elif page == "📚 Notes":
    st.title("📚 Study Notes")
    topic = st.text_input("Enter Topic")

    if st.button("Generate Notes"):
        if topic:
            st.markdown(generate_notes(topic))
        else:
            st.warning("Please enter a topic.")

elif page == "❓ Quiz":
    st.title("❓ Quiz")
    st.write("Quiz section coming soon.")
