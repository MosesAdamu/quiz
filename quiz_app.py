import streamlit as st

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
        "explanation": "Paris has been the capital of France since the 5th century."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars",
        "explanation": "Mars appears red due to iron oxide (rust) on its surface."
    },
    # Add more questions...
]

def display_question():
    """Display current question and options"""
    question_data = questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}")
    st.write(question_data["question"])
    
    # Display options as buttons
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
    """Check if selected answer is correct"""
    question_data = questions[st.session_state.current_question]
    if st.session_state.selected_option == question_data["answer"]:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is: {question_data['answer']}")
    
    st.write(question_data["explanation"])
    
    # Add a continue button
    if st.button("Next Question"):
        next_question()

def next_question():
    """Move to next question or end quiz"""
    st.session_state.selected_option = None
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_complete = True
    st.rerun()

def show_results():
    """Display final score and restart option"""
    st.header("Quiz Complete!")
    st.subheader(f"Your Score: {st.session_state.score}/{len(questions)}")
    
    # Display performance by category if you have categories
    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.rerun()

# Main app logic
st.title("Learning Reinforcement Quiz")

if not st.session_state.quiz_complete:
    display_question()
else:
    show_results()
