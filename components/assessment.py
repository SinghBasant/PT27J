import streamlit as st
import json

class Assessment:
    def __init__(self):
        if 'flagged_questions' not in st.session_state:
            st.session_state.flagged_questions = set()
            
    def render_exam_interface(self):
        # Main content area with question
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_question_panel()
        
        with col2:
            self.render_navigation_panel()
            
            # Submit button should only appear once in the navigation panel
            st.write("---")
            if st.button("Submit Exam", type="primary", key="submit_exam"):
                self.submit_exam()
    
    def render_question_panel(self):
        current_q = st.session_state.questions[st.session_state.current_question_index]
        
        # Question header
        st.write(f"### Question {st.session_state.current_question_index + 1} of {len(st.session_state.questions)}")
        
        # Question content
        st.write(current_q['question'])
        
        # Initialize selected_option
        selected_option = None
        
        # Options
        options = current_q['options']
        if isinstance(options, list):
            # Pre-select the option if it was previously answered
            default_index = None
            if st.session_state.current_question_index in st.session_state.answers:
                default_index = options.index(st.session_state.answers[st.session_state.current_question_index])
            
            selected_option = st.radio(
                "Select your answer:",
                options=options,
                key=f"q_{st.session_state.current_question_index}",
                index=default_index
            )
        
        # Store answer
        if selected_option:
            st.session_state.answers[st.session_state.current_question_index] = selected_option
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Previous", 
                        disabled=st.session_state.current_question_index == 0,
                        key="prev_button"):
                st.session_state.current_question_index -= 1
                st.rerun()
                
        with col2:
            flag_status = st.session_state.current_question_index in st.session_state.flagged_questions
            if st.button("🚩 Flag for Review" if not flag_status else "Remove Flag",
                        key="flag_button"):
                if flag_status:
                    st.session_state.flagged_questions.remove(st.session_state.current_question_index)
                else:
                    st.session_state.flagged_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with col3:
            if st.button("Next ➡️", 
                        disabled=st.session_state.current_question_index == len(st.session_state.questions) - 1,
                        key="next_button"):
                st.session_state.current_question_index += 1
                st.rerun()
    
    def render_navigation_panel(self):
        st.write("### Question Navigator")
        
        # Create grid of question buttons
        cols = st.columns(5)
        for i in range(len(st.session_state.questions)):
            col = cols[i % 5]
            with col:
                button_style = self.get_question_button_style(i)
                if st.button(f"{i + 1}", 
                           key=f"nav_{i}", 
                           **button_style):
                    st.session_state.current_question_index = i
                    st.rerun()
    
    def get_question_button_style(self, question_index):
        style = {}
        
        # Current question
        if question_index == st.session_state.current_question_index:
            style["type"] = "primary"
        
        # Answered question
        elif question_index in st.session_state.answers:
            style["type"] = "secondary"
        
        # Flagged question
        if question_index in st.session_state.flagged_questions:
            style["help"] = "Flagged for review"
        
        return style
    
    def submit_exam(self):
        # Calculate score
        total_questions = len(st.session_state.questions)
        answered_questions = len(st.session_state.answers)
        correct_answers = sum(
            1 for i, answer in st.session_state.answers.items()
            if answer == st.session_state.questions[i]['correct_answer']
        )
        
        # Show results
        st.write("### Assessment Results")
        st.write(f"Total Questions: {total_questions}")
        st.write(f"Answered Questions: {answered_questions}")
        st.write(f"Correct Answers: {correct_answers}")
        st.write(f"Score: {(correct_answers/total_questions)*100:.2f}%")
        
        # Show detailed review
        with st.expander("View Detailed Review"):
            for i, question in enumerate(st.session_state.questions):
                st.write(f"\n**Question {i + 1}**: {question['question']}")
                user_answer = st.session_state.answers.get(i, 'Not answered')
                correct = user_answer == question['correct_answer']
                st.write(f"Your Answer: {user_answer} {'✅' if correct else '❌'}")
                st.write(f"Correct Answer: {question['correct_answer']}")
                st.write(f"Explanation: {question.get('explanation', 'No explanation available.')}")
                st.write("---")
        
        # Reset exam
        if st.button("Start New Assessment", key="reset_exam"):
            for key in ['questions', 'answers', 'start_time', 'exam_in_progress', 
                       'current_question_index', 'flagged_questions']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()