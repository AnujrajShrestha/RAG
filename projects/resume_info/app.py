import streamlit as st
import tempfile
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import PydanticOutputParser

# 1. Page Configuration
st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄", layout="wide")
load_dotenv()

# 2. Pydantic Schema for Structured Output
class ResumeAnalysis(BaseModel):
    name: str
    address: str
    email: Optional[str] = None
    number: Optional[str] = None
    Education: str
    GitHub: Optional[str] = None
    LinkedIn: Optional[str] = None
    Portfolio: Optional[str] = None
    skills: List[str] = []
    projects: Optional[List[str]] = None
    certificates: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    soft_skills: List[str] = []
    language: List[str] = []
    Summary: str
    suggestion: str
    questions: List[str] = []

# 3. LLM and Prompts Initialization
@st.cache_resource
def init_models():
    llm = ChatMistralAI(model='mistral-large-latest')
    embedding_model = MistralAIEmbeddings(model='mistral-embed')
    parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
    return llm, embedding_model, parser

llm, embedding_model, parser = init_models()

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant.
Your task is to analyze the given resume and extract all available information accurately.
Also:
- Summarize the resume.
- Suggest improvements.
- Ask 5 interview questions.

{format_instructions}"""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant.
Your task is to analyze the given resume and Use ONLY the provided context to answer the question.
If the answer is not present in the context, say: "I could not find the answer in the document." """),
    ("human", "Context:\n{context}\n\nQuestion: {question}")
])

# 4. Helper function to process uploaded resume
def process_resume(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    loader = TextLoader(temp_path, encoding='utf-8')
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    
    # Using an ephemeral/in-memory Chroma store per session
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model
    )
    return vector_store

# 5. Streamlit App Layout
st.title("📄 AI Resume Analyzer & Interview Prep")
st.write("Upload a resume in text format to extract key metrics and start a contextual Q&A session.")

# Initialize Session States
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Section")
    uploaded_file = st.file_uploader("Upload Resume (TXT only)", type=["txt"])
    
    if uploaded_file:
        if st.button("Process & Analyze Resume", use_container_width=True):
            with st.spinner("Processing document and generating vector embeddings..."):
                st.session_state.vector_store = process_resume(uploaded_file)
                
                # Perform the primary extraction
                retriever = st.session_state.vector_store.as_retriever(
                    search_type='mmr',
                    search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}
                )
                
                query = "provide the information of this resume."
                docs = retriever.invoke(query)
                context = "\n\n".join(doc.page_content for doc in docs)
                
                formatted_prompt = extraction_prompt.invoke({
                    'context': context,
                    'question': query,
                    "format_instructions": parser.get_format_instructions()
                })
                
                response = llm.invoke(formatted_prompt)
                try:
                    st.session_state.extracted_data = parser.parse(response.content)
                    st.success("Analysis complete!")
                except Exception as e:
                    st.error(f"Failed to parse structured output: {e}")

# 6. Main Dashboard Layout Split
if st.session_state.extracted_data:
    col1, col2 = st.columns([1, 1])
    
    # Left Column: Structured Resume Extraction Content
    with col1:
        st.subheader("📊 Extracted Information")
        data = st.session_state.extracted_data
        
        st.markdown(f"**Name:** {data.name}")
        st.markdown(f"**Address:** {data.address}")
        st.markdown(f"**Email:** {data.email or 'N/A'} | **Phone:** {data.number or 'N/A'}")
        
        st.markdown(f"**🌐 Links:** "
                    f"[GitHub]({data.GitHub or '#'}) | "
                    f"[LinkedIn]({data.LinkedIn or '#'}) | "
                    f"[Portfolio]({data.Portfolio or '#'})")
        
        st.subheader("🎓 Education")
        st.write(data.Education)
        
        st.subheader("💡 Technical & Soft Skills")
        st.write("**Hard Skills:** " + ", ".join(data.skills))
        st.write("**Soft Skills:** " + ", ".join(data.soft_skills))
        st.write("**Languages:** " + ", ".join(data.language))
        
        if data.projects:
            st.subheader("🛠️ Projects")
            for project in data.projects:
                st.markdown(f"- {project}")
                
        st.subheader("📝 Summary")
        st.info(data.Summary)
        
        st.subheader("📈 Suggestions for Improvement")
        st.warning(data.suggestion)
        
        st.subheader("❓ Suggested Interview Questions")
        for q in data.questions:
            st.markdown(f"❓ *{q}*")

    # Right Column: Chat Application Interface
    with col2:
        st.subheader("💬 Ask Questions About the Resume")
        
        # Display chat messages
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)
        
        # Chat input box
        if user_query := st.chat_input("Ask me something about the candidate's experience..."):
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            
            # Fetch context from DB
            retriever = st.session_state.vector_store.as_retriever(
                search_type='mmr',
                search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}
            )
            docs = retriever.invoke(user_query)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            final_prompt = chat_prompt.invoke({
                'context': context,
                'question': user_query
            })
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing context..."):
                    response = llm.invoke(final_prompt)
                    st.write(response.content)
            
            st.session_state.chat_history.append(AIMessage(content=response.content))
else:
    st.info("👈 Please upload and process a text resume from the sidebar to get started.")