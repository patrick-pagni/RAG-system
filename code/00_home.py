import streamlit as st
import os
import ir_datasets
from langchain_core.documents import Document
from simple_rag import SimpleRag

### ENVIRONMENT VARIABLES
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
###

### DOWNLOAD DATA
data = ir_datasets.load("cranfield")
data = [Document(page_content = doc.text, metadata={"title": doc.title, "author": doc.author}) for doc in data.docs_iter()]
###

def get_response():
    simple_rag = SimpleRag()
    st.session_state["response"] = simple_rag(question, data)

st.title("Cranfield Dataset Search Engine")

question = st.text_input("Question:")
st.button("search", on_click = get_response, key = "search")

response = st.empty()

if "response" in st.session_state:
    with response.container():
        st.write(st.session_state["response"])