import json
import streamlit as st
from datetime import datetime

# Load the questions and answers from the JSON file
with open('Sample_Question_Answers.json') as f:
    qa_data = json.load(f)

# Create a dictionary to store the wine information
wine_info = {}

# Loop through the QA data and extract the wine information
for qa in qa_data:
    question = qa['question']
    answer = qa['answer']
    if question.startswith('What is '):
        wine_name = question[8:]
        wine_info[wine_name] = answer

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Determine the greeting based on the time of day
current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "Good morning!"
elif 12 <= current_hour < 18:
    greeting = "Good afternoon!"
else:
    greeting = "Good evening!"

# Add the initial greeting to the conversation history if it's not already there
if not st.session_state.conversation_history:
    st.session_state.conversation_history.append(f'**Bot:** {greeting} How can I help you today?')

# Define a function to handle the user's question
def handle_question(question):
    response_added = False
    # Check if the question is in the QA data
    for qa in qa_data:
        if qa['question'].lower() == question.lower():
            st.session_state.conversation_history.append(f'**Bot:** {qa["answer"]}')
            response_added = True
            break
    # If not, check if the question is about a specific wine
    if not response_added:
        for wine_name, wine_details in wine_info.items():
            if wine_name.lower() in question.lower():
                st.session_state.conversation_history.append(f'**Bot:** {wine_details}')
                response_added = True
                break
    # If not, provide a basic response
    if not response_added:
        if 'hello' in question.lower() or 'hi' in question.lower():
            st.session_state.conversation_history.append('**Bot:** Hello! How can I help you today?')
        elif 'thank' in question.lower() or 'thanks' in question.lower():
            st.session_state.conversation_history.append('**Bot:** You\'re welcome!')
        elif 'how are you' in question.lower():
            st.session_state.conversation_history.append('**Bot:** I\'m doing well, thank you! How can I help you today?')
        else:
            st.session_state.conversation_history.append('**Bot:** Sorry, I didn\'t understand that. Can you please rephrase your question?')

# Create a Streamlit app
st.title('Wine Shop Chatbot')
st.sidebar.title('Questions You Can Ask')

# Display the list of questions the user can ask
for qa in qa_data:
    st.sidebar.markdown(f'- {qa["question"]}')

# Display the conversation history
for message in st.session_state.conversation_history:
    st.markdown(message)

# Create a form for user input
with st.form(key='user_input_form'):
    # Create a text input for the user to ask a question
    user_question = st.text_input('Ask a question:', key='user_question')
    # Add a submit button to the form
    submit_button = st.form_submit_button('Ask')

    # Handle form submission
    if submit_button and user_question:
        # Process the user's question
        st.session_state.conversation_history.append(f'**You:** {user_question}')
        handle_question(user_question)
        # Clear the text input after submission by resetting the form
        st.experimental_rerun()

# Add some styling to the app
st.markdown('<style>body { font-family: Arial; }</style>', unsafe_allow_html=True)
st.markdown('<style>h1 { color: #00698f; }</style>', unsafe_allow_html=True)
st.markdown('<style>p { font-size: 18px; }</style>', unsafe_allow_html=True)
