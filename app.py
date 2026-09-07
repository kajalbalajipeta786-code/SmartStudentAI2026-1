elif page == "📚 Notes":

    st.title("📚 Study Notes")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Notes"):
        if topic:
            st.markdown(generate_notes(topic))
        else:
            st.warning("Please enter a topic.")
