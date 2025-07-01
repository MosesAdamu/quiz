import streamlit as st

# Initialize all session state variables at the start
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
    
    # Use a unique key for the text input
    name = st.text_input("Enter your name to begin:", key="name_input_widget")
    
    # Use a unique key for the button
    if st.button("Start Quiz", key="start_quiz_button"):
        if name.strip():
            # Properly update session state
            st.session_state.quiz.update({
                'user_name': name,
                'user_submitted': True
            })
            st.rerun()
        else:
            st.warning("Please enter your name")

def show_question():
    current_q = st.session_state.quiz['current_question']
    question = questions[current_q]
    
    st.subheader(f"Question {current_q + 1} of {len(questions)}")
    st.image(question["image"], width=300)
    st.write(f"**{question['question']}**")
    
    # Display options with unique keys per question
    cols = st.columns(2)
    for i, option in enumerate(question["options"]):
        if cols[i % 2].button(
            option,
            key=f"q{current_q}_option{i}",
            disabled=st.session_state.quiz['selected_option'] is not None
        ):
            st.session_state.quiz['selected_option'] = option
            check_answer(question)

def check_answer(question):
    if st.session_state.quiz['selected_option'] == question["answer"]:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['answer']}")
    
    st.info(question["explanation"])
    
    # Use a unique key for the continue button
    if st.button("Continue", key=f"continue_{st.session_state.quiz['current_question']}"):
        next_question()

def next_question():
    # Proper state update
    st.session_state.quiz['selected_option'] = None
    if st.session_state.quiz['current_question'] < len(questions) - 1:
        st.session_state.quiz['current_question'] += 1
    else:
        st.session_state.quiz['quiz_complete'] = True
    st.rerun()

def show_results():
    st.header("Quiz Complete!")
    st.subheader(f"Your score: {st.session_state.quiz['score']}/{len(questions)}")
    st.write(f"Well done, {st.session_state.quiz['user_name']}!")
    
    if st.button("Play Again", key="restart_button"):
        # Proper state reset
        st.session_state.quiz.update({
            'current_question': 0,
            'score': 0,
            'selected_option': None,
            'quiz_complete': False
        })
        st.rerun()

# Main app flow - no form elements wrapping state changes
if not st.session_state.quiz['user_submitted']:
    show_landing()
else:
    if not st.session_state.quiz['quiz_complete']:
        show_question()
    else:
        show_results()
