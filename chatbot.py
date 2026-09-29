import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Chat History",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot")

try:
    response = requests.get(f"{API_URL}/chats")
    response.raise_for_status()
    chats = response.json()
except requests.exceptions.RequestException:
    st.error("Unable to connect to the FastAPI backend.")
    st.stop()

with st.sidebar:
    st.header("Chat History")

    new_chat_name = st.text_input(
        "New chat name",
        placeholder="Enter chat name"
    )

    if st.button("New Chat"):
        if new_chat_name.strip():
            response = requests.post(
                f"{API_URL}/chats",
                json={"name": new_chat_name}
            )

            if response.ok:
                new_chat = response.json()
                st.session_state.selected_chat_id = new_chat["id"]
                st.rerun()
        else:
            st.warning("Enter a chat name.")

    st.divider()

    for chat in chats:
        if st.button(
            chat["name"],
            key=chat["id"],
            use_container_width=True
        ):
            st.session_state.selected_chat_id = chat["id"]
            st.rerun()


if "selected_chat_id" not in st.session_state:
    st.info("Create a new chat or select one from the sidebar.")
    st.stop()


selected_chat = next(
    (
        chat
        for chat in chats
        if chat["id"] == st.session_state.selected_chat_id
    ),
    None
)

if selected_chat is None:
    st.info("Select a chat from the sidebar.")
    st.stop()


st.subheader(selected_chat["name"])

file_path = selected_chat["file_path"]

try:
    with open(file_path, "r", encoding="utf-8") as file:
        history = file.read()

    if history:
        st.text(history)

except FileNotFoundError:
    st.warning("Chat history file not found.")


prompt = st.chat_input("Type your message...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(
            f"{API_URL}/chats/{st.session_state.selected_chat_id}/message",
            json={"message": prompt}
        )

        response.raise_for_status()

        assistant_response = response.json()["response"]

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.rerun()

    except requests.exceptions.RequestException:
        st.error("Unable to send message.")