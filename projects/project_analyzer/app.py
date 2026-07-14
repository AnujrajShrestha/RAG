import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

st.set_page_config(
    page_title="Project Analyzer",
    page_icon="📂",
    layout="wide"
)

####################################################
# Models
####################################################

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0
)

embedding_model = MistralAIEmbeddings(
    model="mistral-embed"
)

####################################################
# Output Schema
####################################################

class FolderAnalysis(BaseModel):
    project_name: str = Field(description="Project Name")
    files: List[str]
    path: Optional[str]
    summary: str
    suggestions: str

parser = PydanticOutputParser(
    pydantic_object=FolderAnalysis
)

####################################################
# Prompt
####################################################

summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert software engineer.

Analyze the supplied project.

{format_instructions}
"""
    ),
    (
        "human",
        """
Project Files

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
You are an expert software engineer.

Answer using ONLY the provided project context.

Project Context:

{context}
"""
    ),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

####################################################
# Sidebar
####################################################

st.sidebar.title("📂 Project Analyzer")

uploaded_zip = st.sidebar.file_uploader(
    "Upload Project (.zip)",
    type="zip"
)

####################################################
# Session State
####################################################

if "db" not in st.session_state:
    st.session_state.db = None

if "history" not in st.session_state:
    st.session_state.history = []

####################################################
# Upload & Index
####################################################

if uploaded_zip:

    with tempfile.TemporaryDirectory() as tmpdir:

        zip_path = os.path.join(tmpdir, "project.zip")

        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        extract_dir = os.path.join(tmpdir, "project")

        with zipfile.ZipFile(zip_path) as zip_ref:
            zip_ref.extractall(extract_dir)

        patterns = [
            "**/*.py",
            "**/*.js",
            "**/*.ts",
            "**/*.jsx",
            "**/*.tsx",
            "**/*.html",
            "**/*.css",
            "**/*.json",
            "**/*.md",
            "**/*.txt",
            "**/*.php",
            "**/*.java",
            "**/*.cpp",
            "**/*.c"
        ]

        docs = []

        for pattern in patterns:

            loader = DirectoryLoader(
                extract_dir,
                glob=pattern,
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
                silent_errors=True
            )

            docs.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80
        )

        chunks = splitter.split_documents(docs)

        persist = os.path.join(tmpdir, "db")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory='anaylzer_db'
        )

        st.session_state.db = vectorstore

        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k":8,
                "fetch_k":12,
                "lambda_mult":0.5
            }
        )

        docs = retriever.invoke(
            "Provide project summary."
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = summary_prompt.invoke(
            {
                "context":context,
                "question":"Analyze this project",
                "format_instructions":parser.get_format_instructions()
            }
        )

        response = llm.invoke(prompt)

        analysis = parser.parse(response.content)

        st.title("📂 Project Analysis")

        st.subheader("Project Name")
        st.write(analysis.project_name)

        st.subheader("Files")
        st.write(analysis.files)

        st.subheader("Summary")
        st.write(analysis.summary)

        st.subheader("Suggestions")
        st.write(analysis.suggestions)

        st.divider()

        st.header("💬 Chat with your Project")

        question = st.chat_input("Ask anything...")

        if question:

            st.session_state.history.append(
                HumanMessage(content=question)
            )

            docs = retriever.invoke(question)

            context = "\n\n".join(
                doc.page_content for doc in docs
            )

            prompt = chat_prompt.invoke(
                {
                    "context":context,
                    "question":question,
                    "history":st.session_state.history
                }
            )

            response = llm.invoke(prompt)

            st.session_state.history.append(
                AIMessage(content=response.content)
            )

        for msg in st.session_state.history:

            if isinstance(msg, HumanMessage):

                with st.chat_message("user"):
                    st.write(msg.content)

            else:

                with st.chat_message("assistant"):
                    st.write(msg.content)
                    
del vectorstore
import gc
gc.collect()