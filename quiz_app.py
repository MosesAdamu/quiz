import streamlit as st

# Initialize all session state in a single dictionary
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'current_question': 0,
        'score': 0,
        'selected_option': None,
        'quiz_complete': False,
        'user_name': "",
        'user_submitted': False
    }

# Quiz questions data with direct image URLs
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

def show_landing():
    st.title("Welcome to the Learning Quiz!")
    st.write("Test your knowledge with our interactive quiz")
    
    # Name input with unique key
    name = st.text_input("Enter your name to begin:", key="name_input")
    
    if st.button("Start Quiz", key="start_button"):
        if name.strip():
            st.session_state.quiz.update({
                'user_name': name,
                'user_submitted': True
            })
            st.rerun()
        else:
            st.warning("Please enter your name")

def show_question():
    q = st.session_state.quiz['current_question']
