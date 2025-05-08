from dotenv import load_dotenv
load_dotenv() ## Loading all the environment variables

import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## funtion to load gemini pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text


## Initialize out streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

## When submit is clicked

if submit:
    response = get_gemini_response(input)
    st.subheader("The response is:")
    st.write(response)