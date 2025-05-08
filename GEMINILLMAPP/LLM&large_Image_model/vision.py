from dotenv import load_dotenv
load_dotenv() ## Loading all the environment variables

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## funtion to load gemini pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro")
def get_gemini_response(input,image):
    if input!="":
        response = model.generate_content([input,image])
    else:
        response = model.generate_content(image)
    return response.text


## Initialize out streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("GemininApplication")

input = st.text_input("Input Prompt: ", key="input")
submit = st.button("Ask the question")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jepg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit = st.button("Tell me about the image")

## If submit is clicked

if submit:
    response = get_gemini_response(input, image)
    st.subheader("The response is:")
    st.write(response)