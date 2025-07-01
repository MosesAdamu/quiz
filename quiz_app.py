import streamlit as st
from PIL import Image
import base64

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.quiz_complete = False

# Quiz questions data
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

def display_question():
    question_data = questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}")
    st.write(question_data["question"])
    st.image(question_data["image"], width=300)
    
    cols = st.columns(2)
    for i, option in enumerate(question_data["options"]):
        if cols[i % 2].button(
            option,
            key=f"option_{i}",
            use_container_width=True
        ):
            st.session_state.selected_option = option
            check_answer()

def check_answer():
    question_data = questions[st.session_state.current_question]
    if st.session_state.selected_option == question_data["answer"]:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is: {question_data['answer']}")
    
    st.write(question_data["explanation"])
    
    if st.button("Next Question"):
        next_question()

def next_question():
    st.session_state.selected_option = None
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_complete = True
    st.experimental_rerun()

def show_results():
    st.header("Quiz Complete!")
    st.subheader(f"Your Score: {st.session_state.score}/{len(questions)}")
    
    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.experimental_rerun()

# Main app
st.title("Learning Rei
