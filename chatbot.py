import json
import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Load the questions and answers from the JSON file
with open('Sample_Question_Answers.json') as f:
    data = json.load(f)

# Create a new ChatBot instance
chatbot = ChatBot('Customer Service')

# Train the chatbot with the questions and answers
trainer = ListTrainer(chatbot)
for qa in data:
    trainer.train([qa['question'], qa['answer']])

# Define a function that looks up the appropriate response in the chatbot
def look_up_response(question):
    response = chatbot.get_response(question)
    if response.confidence > 0.5:
        return str(response)
    else:
        return "I'm sorry, I don't have an answer for that question."

# Create a new Streamlit app
st.title('Customer Service Chatbot')
st.subheader('Ask us anything!')

# Define a function for handling user input
def handle_user_input():
    user_question = st.text_input('Question:', '')
    if user_question:
        st.write('**Your question:**', user_question)
        st.write('**Our answer:**', look_up_response(user_question))

# Display the user input form
handle_user_input()
