# 📚 Book Assistant (RAG)

A Retrieval-Augmented Generation (RAG) application built with **LangChain**, **Mistral AI**, **ChromaDB**, and **Streamlit** that allows users to upload PDF books and ask questions based on their contents.

The application converts the uploaded PDF into vector embeddings, stores them in a Chroma vector database, retrieves the most relevant document chunks, and generates accurate answers using Mistral AI.

---

## ✨ Features

- 📄 Upload any PDF book
- ✂️ Automatic document chunking
- 🧠 Mistral AI Embeddings
- 🗄️ Chroma Vector Database
- 🔍 Semantic document retrieval using MMR
- 🤖 AI-powered question answering
- 🌐 Streamlit web interface
- 💻 Command-line version included

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- ChromaDB
- PyPDFLoader
- PyMuPDFLoader
- RecursiveCharacterTextSplitter
- python-dotenv

---

## 📁 Project Structure

```
book-assistance/
│
├── app.py              # Streamlit Web Application
├── db.py               # Creates Vector Database from PDF
├── main.py             # Command Line RAG Chat
├── deeplearning.pdf    # Sample PDF
├── chroma-db/          # Vector database (created automatically)
├── chroma_db/          # Streamlit vector database
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/book-assistance.git

cd book-assistance
```

---

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create a `.env` file

```env
MISTRAL_API_KEY=your_api_key_here
```

---

## ▶️ Running the Streamlit Application

```bash
streamlit run app.py
```

Open your browser and:

1. Upload a PDF.
2. Click **Create Vector Database**.
3. Ask questions about the uploaded document.

---

## ▶️ Running the Command Line Version

### Step 1

Create the vector database

```bash
python db.py
```

### Step 2

Start chatting

```bash
python main.py
```

---

## 🔄 RAG Workflow

```
PDF
   │
   ▼
Document Loader
   │
   ▼
Text Splitter
   │
   ▼
Mistral Embeddings
   │
   ▼
Chroma Vector Database
   │
   ▼
Retriever (MMR Search)
   │
   ▼
Relevant Context
   │
   ▼
Mistral LLM
   │
   ▼
Final Answer
```

---

## 📚 Components Used

### Document Loader

Loads PDF documents.

- PyPDFLoader
- PyMuPDFLoader

---

### Text Splitter

Splits documents into smaller chunks.

```python
RecursiveCharacterTextSplitter
```

Chunk Size:

- 1000 characters

Chunk Overlap:

- 200 characters

---

### Embedding Model

```python
MistralAIEmbeddings(
    model="mistral-embed"
)
```

Converts document chunks into vector embeddings.

---

### Vector Database

```python
Chroma
```

Stores embeddings for semantic similarity search.

---

### Retriever

Uses **Maximum Marginal Relevance (MMR)**.

```python
k = 4
fetch_k = 10
lambda_mult = 0.5
```

This retrieves relevant and diverse document chunks.

---

### Language Model

- mistral-small-2506 (Streamlit app)
- mistral-large-latest (CLI version)

---

## 📷 Streamlit Workflow

```
Upload PDF
      │
      ▼
Create Vector Database
      │
      ▼
Ask Question
      │
      ▼
Retriever
      │
      ▼
Mistral AI
      │
      ▼
Answer
```

---

## Example Questions

- What is deep learning?
- Summarize Chapter 3.
- Explain convolutional neural networks.
- What are the advantages of LSTM?
- What are the key concepts discussed in this book?

---

## Future Improvements

- Support multiple PDFs
- Chat history
- Source citations with page numbers
- Conversation memory
- Hybrid search
- OCR support for scanned PDFs
- FAISS support
- Document summarization
- Multi-file upload
- PDF highlighting

---

## Requirements

```
streamlit
langchain
langchain-community
langchain-mistralai
chromadb
python-dotenv
pymupdf
pypdf
```

---

## Author

Anujraj Shrestha

Learning **Retrieval-Augmented Generation (RAG)**, **LangChain**, **LLMs**, and **AI Application Development** through hands-on projects.

---

## License

This project is intended for educational and learning purposes.