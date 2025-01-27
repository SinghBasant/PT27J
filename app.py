import streamlit as st
from utils.ai_factory import AIFactory
from components.assessment import Assessment
import time
from config import AVAILABLE_MODELS, DEFAULT_MODEL

def main():
    st.set_page_config(
        page_title="Whizzy",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'exam_in_progress' not in st.session_state:
        st.session_state.exam_in_progress = False
    if 'time_limit' not in st.session_state:
        st.session_state.time_limit = 30
    if 'ai_model' not in st.session_state:
        st.session_state.ai_model = DEFAULT_MODEL

    # Sidebar
    with st.sidebar:
        st.header("Exam Configuration")
        
        if not st.session_state.exam_in_progress:
            # AI Model Selection
            st.session_state.ai_model = st.selectbox(
                "Select the AI Model",
                options=["Gemini", "OpenAI"],
                index=0,  # Gemini is default
                help="Choose the AI model for generating questions"
            )
            
            topic = st.text_input("Topic", placeholder="e.g., Python Programming")
            num_questions = st.selectbox("Number of Questions", [1, 5, 10])
            difficulty = st.selectbox("Difficulty🤔Level", ["Easy", "Medium", "Hard"])
            st.session_state.time_limit = st.number_input(
                "Time⏱️ Limit (minutes)", 
                min_value=1, 
                value=30
            )
            
            if st.button("Start Assessment", type="primary"):
                if not topic:
                    st.error("Please enter a topic")
                else:
                    with st.spinner(f"Generating questions using {st.session_state.ai_model}..."):
                        try:
                            ai_provider = AIFactory.get_provider(st.session_state.ai_model)
                            st.session_state.questions = ai_provider.generate_questions(
                                topic, difficulty, num_questions
                            )
                            st.session_state.start_time = time.time()
                            st.session_state.exam_in_progress = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating questions: {str(e)}")
        
        else:
            # Show exam progress
            progress = len(st.session_state.answers) / len(st.session_state.questions)
            st.progress(progress)
            st.write(f"Completed: {progress * 100:.0f}%")
            
            # Time remaining
            elapsed_time = int(time.time() - st.session_state.start_time)
            time_limit_seconds = st.session_state.time_limit * 60
            remaining_time = max(time_limit_seconds - elapsed_time, 0)
            st.write(f"Time Remaining: {remaining_time // 60}:{remaining_time % 60:02d}")

    # Main content area
    if st.session_state.exam_in_progress:
        assessment = Assessment()
        assessment.render_exam_interface()
    else:
        st.title("Whintelz Preps")
        st.header(" Powered by Whizlabs CoI🧠: Center of Intelligence")
        st.write("Configure your assessment parameters in the sidebar to begin.")
        
        st.info("""
        ### Instructions
        - Select your preferred AI model for question generation
        - Select your desired certification or any random topic on 🌏! 
        - Choose number of Qs, the difficulty level.
        - Set an appropriate time limit
        - Click 'Start Assessment' when ready
        - You can mark questions for review [not implemented yet]
        - Submit your exam before the time limit expires [not tested yet]
        """)

if __name__ == "__main__":
    main()