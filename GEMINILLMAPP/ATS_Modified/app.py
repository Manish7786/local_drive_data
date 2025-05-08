import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ""
    return text


## prompt template
input_prompt = """
Hey act like a skilled or very experience ATS(Application tracking system) with deep understanding of tech field,
software engineering, data science, data analyst and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage
Matching based on Job Description and the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%", "MissingKeywords:[]", "Profile Summary":""}}
"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        formatted_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(formatted_prompt)
        # st.subheader("Evaluation Results:")
        st.subheader(response)
        # st.write(response)
        

