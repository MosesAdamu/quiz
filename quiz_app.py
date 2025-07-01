import streamlit as st
from PIL import Image

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.quiz_complete = False
    st.session_state.user_submitted = False
    st.session_state.user_name = ""

# Quiz questions data with images
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "answer": "Paris",
        "explanation": "Paris has been the capital of France since the 5th century.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Paris_-_Eiffelturm_und_Marsfeld2.jpg/800px-Paris_-_Eiffelturm_und_Marsfeld2.jpg"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars",
        "explanation": "Mars appears red due to iron oxide (rust) on its surface.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/OSIRIS_Mars_true_color.jpg/800px-OSIRIS_Mars_true_color.jpg"
    }
]

def landing_page():
    st.title("Welcome to the Learning Quiz!")
    st.markdown("""
    ### Test your knowledge with our interactive quiz
    
    Please enter your name to begin:
    """)
    
    # Collect user name outside of form
    user_name = st.text_input("Your Name", key="name_input")
    
    if st.button("Start Quiz"):
        if user_name:
            st.session_state.user_name = user_name
            st.session_state.user_submitted = True
            st.rerun()
        else:
            st.warning("Please enter your name")

def display_question():
    question_data = questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{question_data['question']}**")
    with col2:
        st.image(question_data["image"], width=200)
    
    cols = st.columns(2)
    for i, option in enumerate(question_data["options"]):
        if cols[i % 2].button(
            option,
            key=f"option_{i}",
            use_container_width=True,
            disabled=st.session_state.selected_option is not None
        ):
            st.session_state.selected_option = option
            check_answer()

def check_answer():
    question_data = questions[st.session_state.current_question]
    if st.session_state.selected_option == question_data["answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question_data['answer']}")
    
    st.info(question_data["explanation"])
    
    if st.button("Continue"):
        next_question()

def next_question():
    st.session_state.selected_option = None
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_complete = True
    st.rerun()

def show_results():
    st.header("Quiz Complete!")
    st.subheader(f"Your Score: {st.session_state.score}/{len(questions)}")
    st.subheader(f"Thanks for playing, {st.session_state.user_name}!")
    
    if st.button("🔄 Take Quiz Again"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.rerun()

# Main app logic
if not st.session_state.user_submitted:
    landing_page()
else:
    st.title(f"Learning Quiz - Welcome, {st.session_state.user_name}!")
    
    if not st.session_state.quiz_complete:
        display_question()
    else:
        show_results()
