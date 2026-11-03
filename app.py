import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from openai import OpenAI
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Interview System",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS - PROFESSIONAL UI
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .question-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .score-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #dddddd;
    }

    .timer-box {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        padding: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "home",
    "candidate_name": "",
    "topic": "Artificial Intelligence",
    "difficulty": "Medium",
    "question_count": 5,
    "questions": [],
    "current_question": 0,
    "results": [],
    "history": [],
    "interview_date": "",
    "mode": "Demo Mode"
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# DEMO QUESTIONS
# ============================================================

demo_questions = {

    "Artificial Intelligence": [
        "What is Artificial Intelligence?",
        "What are the main applications of Artificial Intelligence?",
        "What is the difference between AI and Machine Learning?",
        "What is Deep Learning?",
        "What are the advantages of Artificial Intelligence?"
    ],

    "Machine Learning": [
        "What is Machine Learning?",
        "What is supervised learning?",
        "What is unsupervised learning?",
        "What is overfitting?",
        "What is a confusion matrix?"
    ],

    "Python": [
        "What is Python?",
        "What are Python lists?",
        "What is the difference between a list and a tuple?",
        "What are Python functions?",
        "How do Python generators work?"
    ],

    "Data Analysis": [
        "What is Data Analysis?",
        "What is the purpose of data cleaning?",
        "What is Pandas in Python?",
        "What is data visualization?",
        "What is the difference between mean and median?"
    ],

    "Deep Learning": [
        "What is Deep Learning?",
        "What is a neural network?",
        "What is an activation function?",
        "What is CNN?",
        "What is the purpose of an epoch?"
    ],

    "Cloud Computing": [
        "What is Cloud Computing?",
        "What is IaaS?",
        "What is PaaS?",
        "What is SaaS?",
        "What is the difference between public and private cloud?"
    ]
}


# ============================================================
# HELPER FUNCTION - DEMO EVALUATION
# ============================================================

def demo_evaluate(question, answer):

    answer_length = len(answer.strip().split())

    if answer_length == 0:

        return {
            "Accuracy": 0,
            "Relevance": 0,
            "Completeness": 0,
            "Understanding": 0,
            "Overall": 0,
            "Feedback": "Please provide an answer."
        }

    if answer_length < 8:

        score = 4

    elif answer_length < 20:

        score = 6

    elif answer_length < 40:

        score = 8

    else:

        score = 9

    return {
        "Accuracy": score,
        "Relevance": score,
        "Completeness": max(score - 1, 0),
        "Understanding": score,
        "Overall": score,
        "Feedback":
            "Good attempt. Try to explain the concept with a clear definition and a practical example."
    }


# ============================================================
# HELPER FUNCTION - AI EVALUATION
# ============================================================

def ai_evaluate(question, answer):

    try:

        client = OpenAI()

        prompt = f"""
You are an expert technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer from 0 to 10.

Return exactly:

Accuracy: X
Relevance: X
Completeness: X
Understanding: X
Overall: X
Feedback: short feedback
"""

        response = client.responses.create(
            model="gpt-6-luna",
            input=prompt
        )

        text = response.output_text

        def extract_score(label):

            for line in text.split("\n"):

                if line.lower().startswith(label.lower()):

                    try:

                        value = line.split(":", 1)[1].strip()

                        value = value.replace("/10", "")

                        return float(value)

                    except:

                        return 0

            return 0

        return {
            "Accuracy": extract_score("Accuracy"),
            "Relevance": extract_score("Relevance"),
            "Completeness": extract_score("Completeness"),
            "Understanding": extract_score("Understanding"),
            "Overall": extract_score("Overall"),
            "Feedback": text
        }

    except Exception:

        # If API is unavailable, automatically use demo evaluation
        return demo_evaluate(question, answer)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="main-title">🤖 AI Interview System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered interview practice and performance evaluation</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🎯 Interview Setup")

    col1, col2 = st.columns(2)

    with col1:

        candidate_name = st.text_input(
            "👤 Candidate Name",
            placeholder="Enter your name"
        )

        topic = st.selectbox(
            "📚 Interview Topic",
            list(demo_questions.keys())
        )

        difficulty = st.selectbox(
            "⚡ Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    with col2:

        question_count = st.number_input(
            "📝 Number of Questions",
            min_value=1,
            max_value=5,
            value=5
        )

        mode = st.selectbox(
            "🤖 Interview Mode",
            ["Demo Mode", "AI Mode"]
        )

        st.info(
            "⏱️ Each question has a 2-minute timer."
        )

    st.divider()

    st.subheader("📌 Project Features")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.write("🤖 AI Question Generation")
        st.write("📝 Answer Evaluation")

    with feature2:
        st.write("⏱️ Interview Timer")
        st.write("📊 Performance Analysis")

    with feature3:
        st.write("📈 Score Charts")
        st.write("📥 Report Download")

    st.divider()

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        if candidate_name.strip() == "":

            st.warning("Please enter candidate name.")

        else:

            st.session_state.candidate_name = candidate_name
            st.session_state.topic = topic
            st.session_state.difficulty = difficulty
            st.session_state.question_count = int(question_count)
            st.session_state.mode = mode

            st.session_state.current_question = 0
            st.session_state.results = []

            st.session_state.interview_date = (
                datetime.now().strftime("%d-%m-%Y %H:%M")
            )

            # ------------------------------------------------
            # DEMO MODE
            # ------------------------------------------------

            if mode == "Demo Mode":

                st.session_state.questions = (
                    demo_questions[topic][:int(question_count)]
                )

                st.session_state.page = "interview"

                st.rerun()

            # ------------------------------------------------
            # AI MODE
            # ------------------------------------------------

            else:

                try:

                    client = OpenAI()

                    prompt = f"""
Create {question_count} interview questions.

Topic: {topic}
Difficulty: {difficulty}

Rules:
- Only questions.
- No answers.
- Number questions from 1 to {question_count}.
- Questions should be suitable for a college student.
"""

                    response = client.responses.create(
                        model="gpt-6-luna",
                        input=prompt
                    )

                    generated = response.output_text

                    questions = []

                    for line in generated.split("\n"):

                        line = line.strip()

                        if line:

                            if "." in line[:4]:

                                line = line.split(".", 1)[1].strip()

                            questions.append(line)

                    st.session_state.questions = (
                        questions[:int(question_count)]
                    )

                    st.session_state.page = "interview"

                    st.rerun()

                except Exception as e:

                    st.warning(
                        "AI API unavailable. Switching to Demo Mode so your project can continue."
                    )

                    st.session_state.questions = (
                        demo_questions[topic][:int(question_count)]
                    )

                    st.session_state.mode = "Demo Mode"

                    st.session_state.page = "interview"

                    st.rerun()


# ============================================================
# INTERVIEW PAGE
# ============================================================

elif st.session_state.page == "interview":

    questions = st.session_state.questions

    total_questions = len(questions)

    current = st.session_state.current_question

    question = questions[current]


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🎤 AI Interview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Candidate",
            st.session_state.candidate_name
        )

    with col2:
        st.metric(
            "Topic",
            st.session_state.topic
        )

    with col3:
        st.metric(
            "Difficulty",
            st.session_state.difficulty
        )

    with col4:
        st.metric(
            "Mode",
            st.session_state.mode
        )


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    progress = current / total_questions

    st.progress(progress)

    st.caption(
        f"Question {current + 1} of {total_questions}"
    )


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="question-card">
        <h3>📝 Question {current + 1}</h3>
        <p>{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------

    st.subheader("⏱️ Time Remaining")

    timer_html = """
    <html>

    <body>

    <div id="timer"
    style="
    text-align:center;
    font-size:36px;
    font-weight:bold;
    padding:10px;
    ">
    02:00
    </div>

    <div id="message"
    style="
    text-align:center;
    font-size:18px;
    font-weight:bold;
    ">
    </div>

    <script>

    let time = 120;

    const timer =
        setInterval(function() {

            let minutes =
                Math.floor(time / 60);

            let seconds =
                time % 60;

            document.getElementById("timer")
            .innerHTML =
                String(minutes).padStart(2, "0")
                + ":"
                + String(seconds).padStart(2, "0");

            if (time <= 0) {

                clearInterval(timer);

                document.getElementById("timer")
                .innerHTML = "00:00";

                document.getElementById("message")
                .innerHTML = "⏰ Time's Up!";

            }

            time--;

        }, 1000);

    </script>

    </body>

    </html>
    """

    components.html(
        timer_html,
        height=100
    )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    answer = st.text_area(
        "✍️ Your Answer",
        height=200,
        placeholder="Type your answer here..."
    )


    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    if st.button(
        "✅ Submit Answer",
        use_container_width=True
    ):

        if answer.strip() == "":

            st.warning(
                "Please enter your answer before submitting."
            )

        else:

            with st.spinner(
                "🤖 Evaluating your answer..."
            ):

                if st.session_state.mode == "AI Mode":

                    result = ai_evaluate(
                        question,
                        answer
                    )

                else:

                    result = demo_evaluate(
                        question,
                        answer
                    )


            result["Question"] = question

            result["Answer"] = answer

            st.session_state.results.append(result)


            # ------------------------------------------------
            # NEXT QUESTION
            # ------------------------------------------------

            if current + 1 < total_questions:

                st.session_state.current_question += 1

                st.rerun()

            else:

                st.session_state.page = "result"

                st.rerun()


# ============================================================
# RESULT PAGE
# ============================================================

elif st.session_state.page == "result":

    st.markdown(
        '<div class="main-title">🏆 Interview Result</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="text-align:center;">
        <h3>Candidate: {st.session_state.candidate_name}</h3>
        <p>Topic: {st.session_state.topic}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    df = pd.DataFrame(
        st.session_state.results
    )


    # --------------------------------------------------------
    # AVERAGES
    # --------------------------------------------------------

    final_score = df["Overall"].mean()

    accuracy = df["Accuracy"].mean()

    relevance = df["Relevance"].mean()

    completeness = df["Completeness"].mean()

    understanding = df["Understanding"].mean()


    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    if final_score >= 8:

        performance = "Excellent 🌟"

    elif final_score >= 6:

        performance = "Good 👍"

    elif final_score >= 4:

        performance = "Needs Improvement 📚"

    else:

        performance = "Needs More Practice ❗"


    # --------------------------------------------------------
    # SCORE CARDS
    # --------------------------------------------------------

    st.subheader("📊 Performance Dashboard")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Final Score",
            f"{final_score:.1f}/10"
        )

    with c2:
        st.metric(
            "Accuracy",
            f"{accuracy:.1f}/10"
        )

    with c3:
        st.metric(
            "Relevance",
            f"{relevance:.1f}/10"
        )

    with c4:
        st.metric(
            "Completeness",
            f"{completeness:.1f}/10"
        )

    with c5:
        st.metric(
            "Understanding",
            f"{understanding:.1f}/10"
        )


    st.success(
        f"Performance Level: {performance}"
    )


    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    st.subheader("📈 Question-wise Performance")

    chart_df = df[
        ["Overall"]
    ].copy()

    chart_df.index = [
        f"Q{i + 1}"
        for i in range(len(chart_df))
    ]

    st.bar_chart(chart_df)


    # --------------------------------------------------------
    # CATEGORY CHART
    # --------------------------------------------------------

    st.subheader("📊 Skill Analysis")

    skill_df = pd.DataFrame(
        {
            "Score": [
                accuracy,
                relevance,
                completeness,
                understanding
            ]
        },
        index=[
            "Accuracy",
            "Relevance",
            "Completeness",
            "Understanding"
        ]
    )

    st.bar_chart(skill_df)


    # --------------------------------------------------------
    # DETAILED QUESTIONS
    # --------------------------------------------------------

    st.subheader("📝 Detailed Evaluation")

    for i, row in df.iterrows():

        with st.expander(
            f"Question {i + 1}"
        ):

            st.write(
                f"**Question:** {row['Question']}"
            )

            st.write(
                f"**Your Answer:** {row['Answer']}"
            )

            st.write(
                f"**Accuracy:** {row['Accuracy']}/10"
            )

            st.write(
                f"**Relevance:** {row['Relevance']}/10"
            )

            st.write(
                f"**Completeness:** {row['Completeness']}/10"
            )

            st.write(
                f"**Understanding:** {row['Understanding']}/10"
            )

            st.write(
                f"**Overall:** {row['Overall']}/10"
            )

            st.info(
                row["Feedback"]
            )


    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history_item = {
        "Date": st.session_state.interview_date,
        "Candidate": st.session_state.candidate_name,
        "Topic": st.session_state.topic,
        "Difficulty": st.session_state.difficulty,
        "Score": round(final_score, 1),
        "Performance": performance
    }


    if not st.session_state.history or (
        st.session_state.history[-1]["Date"]
        != history_item["Date"]
    ):

        st.session_state.history.append(
            history_item
        )


    # --------------------------------------------------------
    # INTERVIEW HISTORY
    # --------------------------------------------------------

    st.subheader("📜 Interview History")

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )


    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
AI INTERVIEW SYSTEM
===================

Candidate:
{st.session_state.candidate_name}

Topic:
{st.session_state.topic}

Difficulty:
{st.session_state.difficulty}

Date:
{st.session_state.interview_date}

Interview Mode:
{st.session_state.mode}


FINAL RESULT
============

Final Score:
{final_score:.1f}/10

Performance:
{performance}

Accuracy:
{accuracy:.1f}/10

Relevance:
{relevance:.1f}/10

Completeness:
{completeness:.1f}/10

Understanding:
{understanding:.1f}/10


QUESTION-WISE RESULTS
=====================

"""


    for i, row in df.iterrows():

        report += f"""

Question {i + 1}:
{row['Question']}

Answer:
{row['Answer']}

Accuracy:
{row['Accuracy']}/10

Relevance:
{row['Relevance']}/10

Completeness:
{row['Completeness']}/10

Understanding:
{row['Understanding']}/10

Overall:
{row['Overall']}/10

Feedback:
{row['Feedback']}

---------------------------------------
"""


    st.subheader("📥 Download Report")

    st.download_button(
        label="Download Interview Report",
        data=report,
        file_name="AI_Interview_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


    # --------------------------------------------------------
    # NEW INTERVIEW
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        st.session_state.page = "home"

        st.session_state.questions = []

        st.session_state.current_question = 0

        st.session_state.results = []

        st.rerun()
        