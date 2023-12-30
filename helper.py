import streamlit as st
from openai import OpenAI

from emobots.emobot import Emobot
from emobots.personas import get_all_personas

def initialize_friends():
    personas = get_all_personas()

    friends = {}

    for id, persona in personas.items():
        client = OpenAI(api_key=st.secrets["openai_api_key"])
        name = persona["name"]
        person_desc = persona["description"]

        bot = Emobot(client, name, person_desc)
        friends[id] = bot
        print("Created ", name)

    st.session_state.friends = friends

def show_sidebar():
    with st.sidebar:
        for id, friend in st.session_state.friends.items():
            if st.button(friend.name):
                st.session_state.current_chat_id = id

def show_current_chat_tail():
    friend = st.session_state.friends[st.session_state.current_chat_id]

    for message in friend.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def show_current_chat_head():
    friend = st.session_state.friends[st.session_state.current_chat_id]

    if user_input := st.chat_input("Start typing..."):
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            response_generator = friend.interaction_generator(user_input)

            message_placeholder = st.empty()
            full_response = ""
            for response in response_generator:
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)