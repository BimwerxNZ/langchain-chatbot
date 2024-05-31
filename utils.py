import os
import groq  # Import the Groq client library
import random
import streamlit as st
from datetime import datetime

# decorator
def enable_chat_history(func):
    if os.environ.get("GROQ_API_KEY"):

        # to clear chat history after switching chatbot
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

        # to show chat history on UI
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_groq():
    groq_api_key = st.sidebar.text_input(
        label="Groq API Key",
        type="password",
        value=st.session_state['GROQ_API_KEY'] if 'GROQ_API_KEY' in st.session_state else '',
        placeholder="sk-..."
    )
    if groq_api_key:
        st.session_state['GROQ_API_KEY'] = groq_api_key
        os.environ['GROQ_API_KEY'] = groq_api_key
    else:
        st.error("Please add your Groq API key to continue.")
        st.info("Obtain your key from the Groq platform.")
        st.stop()

    model = "groq-model-name"  # Replace with the default Groq model name
    try:
        client = groq.Client(api_key=groq_api_key)
        available_models = client.models.list()  # Adjust based on the Groq client library
        available_models = sorted(available_models, key=lambda x: x["created"])
        available_models = [i["id"] for i in available_models]

        model = st.sidebar.selectbox(
            label="Model",
            options=available_models,
            index=available_models.index(st.session_state['GROQ_MODEL']) if 'GROQ_MODEL' in st.session_state else 0
        )
        st.session_state['GROQ_MODEL'] = model
    except groq.AuthenticationError as e:
        st.error(e.body["message"])
        st.stop()
    except Exception as e:
        print(e)
        st.error("Something went wrong. Please try again later.")
        st.stop()
    return model

# Example function to use Groq API for generating a response
def generate_response_groq(prompt):
    client = groq.Client(api_key=os.environ.get("GROQ_API_KEY"))
    model = st.session_state['GROQ_MODEL']
    response = client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=150  # Adjust as needed
    )
    return response.choices[0].text.strip()

# Example Streamlit app using Groq API
@enable_chat_history
def chat():
    st.title("Groq Chatbot")
    prompt = st.text_input("You:", "")
    if prompt:
        response = generate_response_groq(prompt)
        display_msg(prompt, "user")
        display_msg(response, "assistant")

if __name__ == "__main__":
    configure_groq()
    chat()
