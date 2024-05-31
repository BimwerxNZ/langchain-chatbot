import utils
import streamlit as st
from streaming import StreamHandler

# Import the appropriate Groq client and LangChain components
from langchain_groq import ChatGroq  # Hypothetical import, replace with actual if available
from langchain.chains import ConversationChain

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Basic Chatbot')
st.write('Allows users to interact with the LLM')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/1_%F0%9F%92%AC_basic_chatbot.py)')

class BasicChatbot:

    def __init__(self):
        self.groq_model = utils.configure_groq()  # Update to use Groq configuration
 
    def setup_chain(self):
        llm = ChatGroq(model_name=self.groq_model, temperature=0, streaming=True)  # Adjust if needed
        chain = ConversationChain(llm=llm, verbose=True)
        return chain
 
    @utils.enable_chat_history  # Ensure this decorator is updated to handle Groq
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = chain.invoke(
                    {"input": user_query},
                    {"callbacks": [st_cb]}
                )
                response = result["response"]
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = BasicChatbot()
    obj.main()
