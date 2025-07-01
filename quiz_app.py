import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import base64

# --- Quiz Data with Images ---
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "answer": "Paris",
        "explanation": "Paris has been the capital of France since the 5th century.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Paris_-_Eiffelturm_und_Marsfeld2.jpg/800px-Paris_-_Eiffelturm_und_Marsfeld2.jpg"
    },
    # ... (include all 10 questions from previous example)
]

# --- File Path for User Data ---
USER_DATA_FILE = "user_data.csv"

# --- Initialize Session State ---
def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.session_state.user_info = None
        st.session_state.user_submitted = False

# --- User Data Collection ---
def collect_user_info():
    st.title("LearnMaster Quiz Registration")
    
    with st.form("user_info_form"):
        st.write("Please provide your details to begin the quiz:")
        
        name = st.text_input("Full Name", key="name")
        email = st.text_input("Email Address", key="email")
        designation = st.selectbox(
            "Designation",
            ["Student", "Teacher", "Researcher", "Professional", "Other"],
            key="designation"
        )
        state = st.text_input("State", key="state")
        lga = st.text_input("Local Government Area (LGA)", key="lga")
        
        submitted = st.form_submit_button("Start Quiz")
        
        if submitted:
            if not all([name, email, designation, state, lga]):
                st.error("Please fill in all fields")
            else:
                st.session_state.user_info = {
                    "name": name,
                    "email": email,
                    "designation": designation,
                    "state": state,
                    "lga": lga,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.user_submitted = True
                
                # Save user data to CSV
                save_user_data(st.session_state.user_info)
                st.rerun()

def save_user_data(user_data):
    """Save user data to CSV file"""
    df = pd.DataFrame([user_data])
    
    if os.path.exists(USER_DATA_FILE):
        existing_df = pd.read_csv(USER_DATA_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(USER_DATA_FILE, index=False)

# --- Quiz Pages ---
def quiz_page():
    st.title("LearnMaster Quiz")
    st.subheader(f"Welcome, {st.session_state.user_info['name']}!")
    
    # Progress bar
    progress = st.session_state.current_question / len(questions)
    st.progress(progress)
    st.caption(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    
    display_question()

def display_question():
    """Display current question and options"""
    question_data = questions[st.session_state.current_question]
    
    # Display question with image
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(question_data["question"])
    with col2:
        st.image(question_data["image"], width=200)
    
    # Display options as buttons
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
    """Check if selected answer is correct"""
    question_data = questions[st.session_state.current_question]
    if st.session_state.selected_option == question_data["answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question_data['answer']}")
    
    st.info(question_data["explanation"])
    
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

def results_page():
    st.header("Quiz Complete!")
    st.subheader(f"Your Score: {st.session_state.score}/{len(questions)}")
    
    # Performance analysis
    st.write("### Performance Summary")
    col1, col2 = st.columns(2)
    col1.metric("Correct Answers", st.session_state.score)
    col2.metric("Accuracy", f"{(st.session_state.score/len(questions))*100:.1f}%")
    
    # Save quiz results
    save_quiz_results()
    
    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_option = None
        st.session_state.quiz_complete = False
        st.rerun()

def save_quiz_results():
    """Save quiz results to user data file"""
    if os.path.exists(USER_DATA_FILE):
        df = pd.read_csv(USER_DATA_FILE)
        
        # Find the user's record (most recent with matching email)
        user_email = st.session_state.user_info["email"]
        user_records = df[df["email"] == user_email]
        
        if not user_records.empty:
            # Update the most recent record
            latest_index = user_records.index[-1]
            df.at[latest_index, "quiz_score"] = st.session_state.score
            df.at[latest_index, "quiz_accuracy"] = (st.session_state.score/len(questions))*100
            df.at[latest_index, "quiz_completed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            df.to_csv(USER_DATA_FILE, index=False)

# --- Main App Logic ---
def main():
    init_session_state()
    
    if not st.session_state.user_submitted:
        collect_user_info()
    else:
        if st.session_state.quiz_complete:
            results_page()
        else:
            quiz_page()

if __name__ == "__main__":
    main()
