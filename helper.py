import random
import streamlit as st

from openai import OpenAI

from emobots.emobot import Emobot
from emobots.personas import get_all_personas
from emobots.random_person import create_random_person_description, create_random_person_description_tinder
from emobots.tools import get_name_from_description

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

def create_random_friend():
    client = OpenAI(api_key=st.secrets["openai_api_key"])

    person_generator = random.choice([
        create_random_person_description,
        create_random_person_description_tinder
    ])

    person_desc = person_generator(client)
    name = get_name_from_description(client, person_desc)
    bot = Emobot(client, name, person_desc)
    id = "random_friend_" + str(len(st.session_state.friends))

    st.session_state.friends[id] = bot


def show_sidebar():
    with st.sidebar:
        if st.button("create random friend"):
            create_random_friend()

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