
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from utils import format_docs

class SimpleRag:
    
    def __call__(self, q, vector_store):

        retriever = vector_store.as_retriever()

        # PROMPT
        prompt = """
            You are a chatbot answering questions on The Cranfield dataset corpus. Using these retrieved documents as context: {context}

            Answer this question: {question}
        """
        prompt = ChatPromptTemplate.from_template(prompt)

        llm = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature = 0)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(q)

        return response