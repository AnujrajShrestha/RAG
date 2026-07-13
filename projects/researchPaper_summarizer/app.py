import os
import shutil
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
import uuid

db_path = f"summarizer_db/{uuid.uuid4()}"

load_dotenv()

st.set_page_config(
    page_title="Research Paper Summarizer",
    page_icon="📄",
    layout="wide"
)

llm = ChatMistralAI(
    model="mistral-large-latest"
)

embedding_model = MistralAIEmbeddings(
    model="mistral-embed"
)

summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI research assistant.

        Summarize the research paper into three detailed paragraphs.

        Cover:
        - Main objective
        - Methodology
        - Results
        - Conclusion
        """
    ),
    (
        "human",
        """
        Context:
        {context}

        Question:
        {question}
        """
    )
])

chat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI assistant.

        Use ONLY the provided context.

        If the answer cannot be found in the document,
        say:

        I could not find the answer in the document.
        """
    ),
    (
        "human",
        """
        Context:
        {context}

        Question:
        {question}
        """
    )
])

st.title("📄 Research Paper Summarizer & Chat")

uploaded_pdf = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_pdf:

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    pdf_path = temp_dir / uploaded_pdf.name

    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_path
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":12,
            "fetch_k":20,
            "lambda_mult":0.5
        }
    )

    st.success("PDF processed successfully!")

    if st.button("Generate Summary"):

        docs = retriever.invoke(
            "Summarize the research paper."
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = summary_prompt.invoke({
            "context": context,
            "question":"Summarize this paper in three paragraphs."
        })

        response = llm.invoke(prompt)

        st.subheader("Summary")

        st.write(response.content)

    st.divider()

    st.subheader("Chat with Paper")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_question = st.chat_input(
        "Ask anything about the paper..."
    )

    if user_question:

        with st.chat_message("user"):
            st.markdown(user_question)

        docs = retriever.invoke(user_question)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = chat_prompt.invoke({
            "context": context,
            "question": user_question
        })

        response = llm.invoke(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.content)

        st.session_state.messages.append(
            {
                "role":"user",
                "content":user_question
            }
        )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":response.content
            }
        )