import streamlit as st

from openai import OpenAI

from emobots.emobot import Emobot
from emobots.personas import get_all_personas

st.title("Friendface")

if st.button('Reset'):
    st.session_state.messages = []
    st.session_state.chat_messages = []


if "friends" not in st.session_state:
    personas = get_all_personas()

    friends = {}

    for id, persona in personas.items():
        api_key = ""
        client = OpenAI(api_key=api_key)
        name = persona["name"]
        person_desc = persona["description"]

        bot = Emobot(client, name, person_desc)
        friends[id] = bot
        print("Created ", name)

    st.session_state.friends = friends

if "current_chat_id" not in st.session_state:
    # get first entry in dictiorary
    st.session_state.current_chat_id = list(st.session_state.friends.keys())[0]

with st.sidebar:
    for id, friend in st.session_state.friends.items():
        if st.button(friend.name):
            st.session_state.current_chat_id = id

st.markdown(st.session_state.current_chat_id)

friend = st.session_state.friends[st.session_state.current_chat_id]


for message in friend.chat_messages:
    #st.image(image, caption="vampire", width=100)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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