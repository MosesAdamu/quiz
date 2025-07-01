import streamlit as st
from PIL import Image

# Initialize all session state variables at the start
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {
        'current_question': 0,
        'score': 0,
        'selected_option': None,
        'quiz_complete': False,
        'user_submitted': False,
        'user_name': ""
    }

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
    
    # Use a separate key for the text input widget
    name_input = st.text_input("Your Name", key="name_input_widget")
    
    if st.button("Start Quiz", key="start_quiz_button"):
        if name_input:
            st.session_state.quiz_data.update({
                'user_name': name_input,
                'user_submitted': True
            })
            st.rerun()
        else:
            st.warning("Please enter your name")

def display_question():
    current = st.session_state.quiz_data['current_question']
    question_data = questions[current]
    
    st.subheader(f"Question {current + 1} of {len(questions)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{question_data['question']}**")
    with col2:
        st.image(question_data["image"], width=200)
    
    cols = st.columns(2)
    for i, option in enumerate(question_data["options"]):
        if cols[i % 2].button(
            option,
            key=f"option_{current}_{i}",  # Unique key per question
            use_container_width=True,
            disabled=st.session_state.quiz_data['selected_option'] is not None
        ):
            st.session_state.quiz_data['selected_option'] = option
            check_answer()

def check_answer():
    current = st.session_state.quiz_data['current_question']
    question_data = questions[current]
    selected = st.session_state.quiz_data['selected_option']
    
    if selected == question_data["answer"]:
        st.session_state.quiz_data['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question_data['answer']}")
    
    st.info(question_data["explanation"])
    
    if st.button("Continue", key=f"continue_{current}"):
        next_question()

def next_question():
    quiz_data = st.session_state.quiz_data
    quiz_data['selected_option'] = None
    if quiz_data['current_question'] < len(questions) - 1:
        quiz_data['current_question'] += 1
    else:
        quiz_data['quiz_complete'] = True
    st.rerun()

def show_results():
    quiz_data = st.session_state.quiz_data
    st.header("Quiz Complete!")
    st.subheader(f"Your Score: {quiz_data['score']}/{len(questions)}")
    st.subheader(f"Thanks for playing, {quiz_data['user_name']}!")
    
    if st.button("🔄 Take Quiz Again", key="restart_quiz"):
        quiz_data.update({
            'current_question': 0,
            'score': 0,
            'selected_option': None,
            'quiz_complete': False
        })
        st.rerun()

# Main app logic
if not st.session_state.quiz_data['user_submitted']:
    landing_page()
else:
    st.title(f"Learning Quiz - Welcome, {st.session_state.quiz_data['user_name']}!")
    
    if not st.session_state.quiz_data['quiz_complete']:
        display_question()
    else:
        show_results()
