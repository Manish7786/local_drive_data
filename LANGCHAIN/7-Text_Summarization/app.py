import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import pytube

# Streamlit app configuration
st.set_page_config(page_title="Langchain: Summarize Text from YT or Website")
st.title("Langchain: Summarize Text from YT or Website")
st.subheader("Summarize URL")

# Sidebar: Get API key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# Main input: URL
generic_url = st.text_input("Enter URL (YouTube or Website)", label_visibility="collapsed")

# Initialize LLM
if groq_api_key:
    llm = ChatGroq(groq_api_key=groq_api_key, model="gemma-7b-it")
else:
    st.error("Groq API Key is missing")
    st.stop()

# Prompt template
prompt_template = """
Provide a summary of following content in 300 words:
content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Button to summarize
if st.button("Summarize the content from YT or Website"):
    # Input validation
    if not generic_url.strip():
        st.error("Please provide a valid URL to summarize")
    elif not validators.url(generic_url):
        st.error("The URL provided is invalid. It must be a valid YouTube or Website URL.")
    else:
        try:
            with st.spinner("Loading and summarizing content..."):
                # Select the appropriate loader
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        },
                    )
                
                # Load documents
                try:
                    docs = loader.load()
                except Exception as load_err:
                    st.error(f"Failed to load content from the URL: {load_err}")
                    st.stop()
                
                # Summarize using the chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                # Display summary
                st.success("Summary:")
                st.write(output_summary)

        except Exception as e:
            st.error("An unexpected error occurred during summarization.")
            st.exception(e)
