import time
import os
import joblib
import streamlit as st
import google.generativeai as genai 
from dotenv import load_dotenv

load_dotenv()

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = f'{time.time()}'
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'


CUSTOM_API_KEY = os.environ.get('AIzaSyAQ_P5U9JSvjZk2MGO8DQayHe1Z1yftQZI')  
genai.configure(api_key=CUSTOM_API_KEY) 

MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🤖'


try:
    os.mkdir('data/')
except FileExistsError:
    pass


try:
    past_chats = joblib.load('data/past_chats_list')
except FileNotFoundError:
    past_chats = {}


with st.sidebar:
    st.write('# Previous Chats')
    st.session_state.chat_id = st.selectbox(
        label='Pick a past chat',
        options=[st.session_state.chat_id] + list(past_chats.keys()),
        index=0,
        format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
        placeholder='_',
    )
    st.session_state.chat_title = past_chats.get(st.session_state.chat_id, f'ChatSession-{st.session_state.chat_id}')

st.write('# Chat with Talkie!')


try:
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    st.session_state.chat_history = joblib.load(f'data/{st.session_state.chat_id}-chat_messages')
    print('old cache')
except FileNotFoundError:
    st.session_state.messages = []
    st.session_state.chat_history = []
    print('new_cache made')


st.session_state.model = genai.GenerativeModel('gemini-pro') 
st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.chat_history)


for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

def replace_name_and_trainer(response_text):
    response_text = response_text.replace("Gemini", "Talkie")
    response_text = response_text.replace("Google", "Team Brackets")
    return response_text


if prompt := st.chat_input('Ask me Anything...'):

    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append(dict(role='user', content=prompt))

    response = st.session_state.chat.send_message(prompt, stream=True)

    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response

        for chunk in response:
            full_response += chunk.text + ' '
            message_placeholder.write(full_response + '▌')

        full_response = replace_name_and_trainer(full_response)
        message_placeholder.write(full_response)

    st.session_state.messages.append(
        dict(role=MODEL_ROLE, content=full_response.strip(), avatar=AI_AVATAR_ICON)
    )
    st.session_state.chat_history = st.session_state.chat.history

    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.chat_history, f'data/{st.session_state.chat_id}-chat_messages')