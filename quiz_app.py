import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime

# Initialize session state
def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.session_state.user_info = None
        st.session_state.user_submitted = False

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
    },
    {
        "question": "What is the largest mammal on Earth?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "answer": "Blue Whale",
        "explanation": "Blue whales can reach lengths of up to 100 feet and weigh 200 tons.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg/800px-Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg"
    }
]

def landing_page():
    st.title("Welcome to the Learning Quiz!")
    st.markdown("""
    ### Test your knowledge with our interactive quiz
    
    Features:
    - 📝 Multiple choice questions
    - 🖼️ Visual aids with images
    - 📊 Instant feedback and explanations
    - 🏆 Track your score
    
    Ready to begin?
    """)
    
    with st.form("user_info"):
        name = st.text_input("Your Name")
        email = st.text_input("Email (optional)")
        if st.form_submit_button("Start Quiz"):
            if name:  # Only require name
                st.session_state.user_info = {
                    "name": name,
                    "email": email,
                    "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.user_submitted = True
                st.rerun()
            else:
                st.warning("Please enter at least your name")

def display_question():
    question_data = questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    
    # Display question with image
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{question_data['question']}**")
    with col2:
        st.image(question_data["image"], width=200)
    
    # Display options
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
    
    # Calculate percentage
    percentage = (st.session_state.score / len(questions)) * 100
    st.metric("Accuracy", f"{percentage:.1f}%")
    
    if st.button("🔄 Take Quiz Again"):
        # Reset quiz but keep user info
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.rerun()

# Main app logic
init_session_state()

if not st.session_state.user_submitted:
    landing_page()
else:
    st.title(f"Learning Quiz - Welcome, {st.session_state.user_info['name']}!")
    
    if not st.session_state.quiz_complete:
        display_question()
    else:
        show_results()
