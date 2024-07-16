# wine-chatbot

This is a simple Wine Shop Chatbot built using Streamlit. The chatbot can respond to questions about different wines, provide general responses, and greet users based on the time of day.

## Features

- Greet users based on the time of day (morning, afternoon, evening).
- Respond to predefined questions from a JSON file.
- Provide information about specific wines.
- Basic responses for common greetings and thanks.
- Display conversation history.

## Requirements

- Python 3.7 or higher
- Streamlit
- JSON file containing questions and answers (`Sample_Question_Answers.json`)

## Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/yourusername/wine-shop-chatbot.git
    cd wine-shop-chatbot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install streamlit
    ```

## Usage

1. Create a `Sample_Question_Answers.json` file in the project directory with the following structure:

    ```json
    [
        {
            "question": "What is Wine A?",
            "answer": "Wine A is a red wine with rich flavor."
        },
        {
            "question": "What is Wine B?",
            "answer": "Wine B is a white wine with a crisp taste."
        }
    ]
    ```

2. Run the Streamlit app:

    ```sh
    streamlit run chatbot.py
    ```

3. Open your web browser and go to `http://localhost:8501` to interact with the chatbot.

## Code Explanation

The main script `chatbot.py` includes:

1. **Imports and Data Loading**:
    ```python
    import json
    import streamlit as st
    from datetime import datetime

    with open('Sample_Question_Answers.json') as f:
        qa_data = json.load(f)
    ```

2. Wine Information Extraction**:
    ```python
    wine_info = {}
    for qa in qa_data:
        question = qa['question']
        answer = qa['answer']
        if question.startswith('What is '):
            wine_name = question[8:]
            wine_info[wine_name] = answer
    ```

3. Session State Initialization**:
    ```python
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    ```

4. Greeting Based on Time**:
    ```python
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    if not st.session_state.conversation_history:
        st.session_state.conversation_history.append(f'**Bot:** {greeting} How can I help you today?')
    ```

5. Question Handling Function**:
    ```python
    def handle_question(question):
        response_added = False
        for qa in qa_data:
            if qa['question'].lower() == question.lower():
                st.session_state.conversation_history.append(f'**Bot:** {qa["answer"]}')
                response_added = True
                break
        if not response_added:
            for wine_name, wine_details in wine_info.items():
                if wine_name.lower() in question.lower():
                    st.session_state.conversation_history.append(f'**Bot:** {wine_details}')
                    response_added = True
                    break
        if not response_added:
            if 'hello' in question.lower() or 'hi' in question.lower():
                st.session_state.conversation_history.append('**Bot:** Hello! How can I help you today?')
            elif 'thank' in question.lower() or 'thanks' in question.lower():
                st.session_state.conversation_history.append('**Bot:** You\'re welcome!')
            elif 'how are you' in question.lower():
                st.session_state.conversation_history.append('**Bot:** I\'m doing well, thank you! How can I help you today?')
            else:
                st.session_state.conversation_history.append('**Bot:** Sorry, I didn\'t understand that. Can you please rephrase your question?')
    ```

6. Streamlit App Layout**:
    ```python
    st.title('Wine Shop Chatbot')
    st.sidebar.title('Questions You Can Ask')

    for qa in qa_data:
        st.sidebar.markdown(f'- {qa["question"]}')

    for message in st.session_state.conversation_history:
        st.markdown(message)

    with st.form(key='user_input_form'):
        user_question = st.text_input('Ask a question:', key='user_question')
        submit_button = st.form_submit_button('Ask')

        if submit_button and user_question:
            st.session_state.conversation_history.append(f'**You:** {user_question}')
            handle_question(user_question)
            st.experimental_rerun()
    ```

7. Styling**:
    ```python
    st.markdown('<style>body { font-family: Arial; }</style>', unsafe_allow_html=True)
    st.markdown('<style>h1 { color: #00698f; }</style>', unsafe_allow_html=True)
    st.markdown('<style>p { font-size: 18px; }</style>', unsafe_allow_html=True)
    ```

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.


