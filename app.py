import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

st.set_page_config(page_title="Smart Student AI", page_icon="🎓")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Add GOOGLE_API_KEY in your app's Settings > Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3.8-flash")


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


def generate_plan(assignments, practicals, tests, exam_date, study_hours):
    prompt = (
        "Create a realistic day-by-day study and task plan for a student based on this info:\n"
        f"Assignments due: {assignments}\n"
        f"Practical records to complete: {practicals}\n"
        f"Daily slip tests: {tests}\n"
        f"Mid-semester exam date: {exam_date}\n"
        f"Available study time per day: {study_hours} hours\n\n"
        "Prioritize by deadline and urgency. Organize the plan day by day, "
        "clearly listing what to do each day. Keep it realistic and not overloaded."
    )
    return ask_ai(prompt)


def simplify_question(question):
    prompt = (
        f"A student is confused by this question: \"{question}\"\n\n"
        "Provide, in this order:\n"
        "1. A simple-English explanation of what it means\n"
        "2. Meanings of any difficult words\n"
        "3. A breakdown of what the question is actually asking\n"
        "4. Step-by-step guidance to answer it\n"
        "5. A short example\n"
        "6. One short question to check the student's understanding"
    )
    return ask_ai(prompt)


def make_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)
    pdf.set_font("Helvetica", size=12)
    safe_text = content.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 8, safe_text)
    return bytes(pdf.output())


def pdf_download_button(label, title, content, filename):
    pdf_bytes = make_pdf(title, content)
    st.download_button(
        label=label,
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )


page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "📝 Notes", "❓ Quiz", "🎮 Games", "📅 Daily Planner", "🧠 Question Simplifier"],
)

if page == "🏠 Home":
    st.title("Welcome to Smart Student AI")
    st.write("Pick a feature from the sidebar, enter your details, and get real AI-generated help.")

elif page == "📝 Notes":
    st.title("Study Notes Generator")
    topic = st.text_input("Enter a topic")
    if st.button("Generate Notes") and topic:
        with st.spinner("Generating notes..."):
            notes = generate_notes(topic)
        st.markdown(notes)
        pdf_download_button("⬇️ Download Notes as PDF", f"Study Notes: {topic}", notes, "notes.pdf")

elif page == "❓ Quiz":
    st.title("Quiz Generator")
    topic = st.text_input("Enter a topic")
    if st.button("Generate Quiz") and topic:
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(topic)
        st.markdown(quiz)
        pdf_download_button("⬇️ Download Quiz as PDF", f"Quiz: {topic}", quiz, "quiz.pdf")

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

elif page == "📅 Daily Planner":
    st.title("Smart Daily Planner")
    assignments = st.text_area("Assignments and due dates")
    practicals = st.text_area("Practical records to complete")
    tests = st.text_area("Daily slip tests")
    exam_date = st.text_input("Mid-semester exam date")
    study_hours = st.number_input("Available study time per day (hours)", min_value=1, max_value=16, value=3)

    if st.button("Generate Plan"):
        with st.spinner("Building your plan..."):
            plan = generate_plan(assignments, practicals, tests, exam_date, study_hours)
        st.markdown(plan)
        pdf_download_button("⬇️ Download Plan as PDF", "My Study Plan", plan, "study_plan.pdf")

elif page == "🧠 Question Simplifier":
    st.title("AI Question Simplifier")
    question = st.text_area("Paste a difficult question here")
    if st.button("Simplify") and question:
        with st.spinner("Breaking it down..."):
            simplified = simplify_question(question)
        st.markdown(simplified)
        pdf_download_button("⬇️ Download Explanation as PDF", "Question Explained", simplified, "explanation.pdf")
