import streamlit as st
from datetime import datetime

# Set page configuration to open the sidebar automatically
st.set_page_config(page_title="Bluff_ChatSpace", page_icon="♠️", initial_sidebar_state="expanded")


# Initialize session state variables
if 'public_chat' not in st.session_state:
    st.session_state.public_chat = []
if 'private_chats' not in st.session_state:
    st.session_state.private_chats = {}

# Function to display chat messages
def display_chat(chat_history):
    for message in chat_history:
        st.markdown(f"**{message['user']}** [{message['time']}] : {message['message']}")

# Function to send a message in public or private chat
def send_message(user, message, chat_type, private_recipient=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_message = {'user': user, 'message': message, 'time': timestamp}
    
    if chat_type == 'Public':
        st.session_state.public_chat.append(chat_message)
    else:
        if private_recipient not in st.session_state.private_chats:
            st.session_state.private_chats[private_recipient] = []
        st.session_state.private_chats[private_recipient].append(chat_message)

# User input section
st.sidebar.title("Chat Login")
username = st.sidebar.text_input("Enter your name", key="user")

if username:
    st.sidebar.success(f"Logged in as {username}")
    
    # Choose between public or private chat
    chat_type = st.selectbox("Select Chat Type", ['Public', 'Private'])

    if chat_type == 'Public':
        st.header("Public Chat Room")
        display_chat(st.session_state.public_chat)

        # Public chat input
        public_message = st.text_input("Enter message for public chat:")
        if st.button("Send to Public Chat"):
            if public_message:
                send_message(username, public_message, chat_type)
            else:
                st.warning("Please enter a message before sending.")

    elif chat_type == 'Private':
        st.header("Private Chat Room")
        
        # Private chat section
        recipient = st.text_input("Recipient's name:")
        
        if recipient:
            if recipient in st.session_state.private_chats:
                display_chat(st.session_state.private_chats[recipient])
            else:
                st.write(f"No messages found for {recipient}. Start a conversation!")

            # Private chat input
            private_message = st.text_input("Enter message for private chat:")
            if st.button("Send to Private Chat"):
                if private_message:
                    send_message(username, private_message, chat_type, recipient)
                else:
                    st.warning("Please enter a message before sending.")

else:
    st.warning("Please enter a username to continue.")
