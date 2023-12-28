import streamlit as st


import helper

st.title("Friendface")

if st.button('Reset'):
    st.session_state.messages = []
    st.session_state.chat_messages = []


if "friends" not in st.session_state:
    helper.initialize_friends()


if "current_chat_id" not in st.session_state:
    # get first entry in dictiorary
    st.session_state.current_chat_id = list(st.session_state.friends.keys())[0]

helper.show_sidebar()

friend = st.session_state.friends[st.session_state.current_chat_id]

st.markdown(f"You are chatting with *{friend.name}*.")

helper.show_current_chat_tail()

helper.show_current_chat_head()

