import os
import ir_datasets
import pickle
import sys

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from simple_rag import SimpleRag

### ENVIRONMENT VARIABLES
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
###

### DOWNLOAD DATA
filepath = "../data/cranfield_docs_db"
my_file = Path(filepath)
print(os.getcwd())
if my_file.is_dir():
    vector_store = Chroma(
        collection_name="cranfield_docs",
        embedding_function = OpenAIEmbeddings(),
        persist_directory="./cranfield_docs_db"  # Directory where data is saved
    )

else:
    data = ir_datasets.load("cranfield")
    data = [Document(page_content = doc.text, metadata={"title": doc.title, "author": doc.author}) for doc in data.docs_iter()]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = text_splitter.split_documents(data)

    vector_store = Chroma(
        collection_name="cranfield_docs",
        embedding_function=OpenAIEmbeddings(),  # Replace with your embedding function
        persist_directory="../data/cranfield_docs_db"  # Directory to save data
    )

    vector_store.add_documents(splits)
###

simple_rag = SimpleRag()

output = simple_rag(sys.argv[1], vector_store)

print(output)