page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "📚 Notes", "❓ Quiz"]
)

if page == "🏠 Home":
    st.title("Home")

elif page == "📚 Notes":
    st.title("📚 Study Notes")
    topic = st.text_input("Enter Topic")
    if st.button("Generate Notes"):
        if topic:
            st.markdown(generate_notes(topic))
        else:
            st.warning("Please enter a topic.")

elif page == "❓ Quiz":
    st.title("Quiz")
