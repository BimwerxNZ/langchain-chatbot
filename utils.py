import os
import streamlit as st
import groq  # Import the Groq client library

def enable_chat_history(func):
    if os.environ.get("GROQ_API_KEY"):
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_groq():
    groq_api_key = st.sidebar.text_input(
        label="Groq API Key",
        type="password",
        value=st.session_state['GROQ_API_KEY'] if 'GROQ_API_KEY' in st.session_state else '',
        placeholder="gsk_-..."
    )
    if groq_api_key:
        st.session_state['GROQ_API_KEY'] = groq_api_key
        os.environ['GROQ_API_KEY'] = groq_api_key
    else:
        st.error("Please add your Groq API key to continue.")
        st.info("Obtain your key from the Groq platform.")
        st.stop()

    model = "mixtral-8x7b-32768"  # Replace with the default Groq model name
    
    return model
