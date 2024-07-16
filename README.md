# Talkie Chatbot

## Overview

This project is a Streamlit-based chat application that interacts with the talkie AI model, allowing users to engage in conversations with an artificial intelligence assistant. The application stores chat history, allowing users to revisit and continue previous conversations.


## Getting Started

### Dependencies

This code uses the following libraries:

- `streamlit`: for building the user interface. 
- `talkie`: for chat 


### Usage

Follow these steps to set up and run the project:

1. Create a virtual environment:
```
python3 -m venv my_env
source my_env/bin/activate 
.\my_env\Scripts\activate 
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the Streamlit server:
```
streamlit run app_chat.py
```

4. Access the application in your browser at http://localhost:8501.

5. Start chatting with the assistant!



## How it Works

The app as follows:

1. The user enters a question in the input field.

2. User messages are sent to the talkie model for processing.

3. The user's input, along with the chat history, is used to generate a response.

4. The talkie model generates a response based on the patterns it learned during training.

5. The application saves chat messages and talkie AI chat history to files for later retrieval.

6. A new chat is created if the user initiates a conversation that hasn't been stored before, or user can go back to past chats.
