import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Smart Student AI", page_icon="🎓")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in your app's Settings > Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(prompt):
    """Send a prompt to Gemini and return the text reply."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


def generate_notes(topic):
    prompt = f"Write clear, well-organized study notes on the topic: {topic}. Use headings and bullet points."
    return ask_ai(prompt)


def generate_quiz(topic):
    prompt = (
        f"Create a short 5-question quiz on the topic: {topic}. "
        "Mix multiple choice and short answer. Include the answer key at the end."
    )
    return ask_ai(prompt)


def generate_game_question(topic):
    prompt = (
        f"Create ONE multiple choice trivia question about {topic} for a student game. "
        "Format exactly like this:\n"
        "Question: <question text>\n"
        "A) <option>\nB) <option>\nC) <option>\nD) <option>\n"
        "Answer: <correct letter only>"
    )
    return ask_ai(prompt)


page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "📝 Notes", "❓ Quiz", "🎮 Games"],
)

if page == "🏠 Home":
    st.title("Welcome to Smart Student AI")
    st.write("Pick **Notes**, **Quiz**, or **Games** from the sidebar, enter a topic, and get real AI-generated help.")

elif page == "📝 Notes":
    st.title("Study Notes Generator")
    topic = st.text_input("Enter a topic")
    if st.button("Generate Notes") and topic:
        with st.spinner("Generating notes..."):
            notes = generate_notes(topic)
        st.markdown(notes)

elif page == "❓ Quiz":
    st.title("Quiz Generator")
    topic = st.text_input("Enter a topic")
    if st.button("Generate Quiz") and topic:
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(topic)
        st.markdown(quiz)

elif page == "🎮 Games":
    st.title("Trivia Game")
    topic = st.text_input("Pick a topic to play")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "game_q" not in st.session_state:
        st.session_state.game_q = None

    if st.button("New Question") and topic:
        with st.spinner("Loading question..."):
            st.session_state.game_q = generate_game_question(topic)

    if st.session_state.game_q:
        st.markdown(st.session_state.game_q.split("Answer:")[0])
        user_answer = st.radio("Your answer:", ["A", "B", "C", "D"])
        if st.button("Submit Answer"):
            correct = st.session_state.game_q.split("Answer:")[-1].strip()[0].upper()
            if user_answer == correct:
                st.success("Correct! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"Wrong — correct answer was {correct}")
            st.write(f"Score: {st.session_state.score}")
