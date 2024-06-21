from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    # Concatenate response chunks into a single line
    return " ".join([chunk.text for chunk in response])

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo", page_icon=":robot:", layout="wide")

# Add custom CSS styles
with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.header("Q&A Chatbot")
st.write("")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_field = st.text_input("Input: ", key="input", placeholder="Ask me anything...")
submit_button = st.button("Ask the question", help="Get an answer from Gemini Pro")

if submit_button and input_field:
    response = get_gemini_response(input_field)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_field))
    st.session_state['chat_history'].append(("Bot", response))
    
    st.subheader("The Response is")
    st.write(response)

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

# Add a footer with a link to the Gemini Pro model
st.write("")
st.write("Powered by [Gemini Pro](https://generative.ai/models/gemini-pro)")
