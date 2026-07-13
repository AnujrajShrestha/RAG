import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma

load_dotenv()

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Enterprise Policy Assistant",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Enterprise Policy Assistant")
st.caption("Ask questions related to your company policies.")

# ----------------------------
# Load Models (Cached)
# ----------------------------

@st.cache_resource
def load_rag():

    embedding = MistralAIEmbeddings(
        model="mistral-embed"
    )

    vectorstore = Chroma(
        persist_directory="Entreprise_db",
        embedding_function=embedding
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":4,
            "fetch_k":10,
            "lambda_mult":0.5
        }
    )

    llm = ChatMistralAI(
        model="mistral-large-latest"
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not found in the context, reply exactly:

"I could not find the answer in the document."

Answer only company related questions.
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

    return retriever, llm, prompt


retriever, llm, prompt = load_rag()

# ----------------------------
# Chat History
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# User Input
# ----------------------------

question = st.chat_input("Ask a company policy question...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    final_prompt = prompt.invoke({
        "context":context,
        "question":question
    })

    response = llm.invoke(final_prompt)

    with st.chat_message("assistant"):
        st.markdown(response.content)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response.content
        }
    )

    with st.expander("Retrieved Context"):
        st.write(context)