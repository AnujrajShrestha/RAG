# 📄 AI Resume Analyzer using RAG

An AI-powered Resume Analyzer built with **Python, Streamlit, LangChain, ChromaDB, and Mistral AI**. The application uses **Retrieval-Augmented Generation (RAG)** to analyze resumes, extract structured information, answer questions about the uploaded resume, and provide suggestions for improvement.

---

## ✨ Features

* 📄 Upload a resume in **TXT** format.
* 🧠 Automatically extract:

  * Personal Information
  * Contact Details
  * Education
  * Skills
  * Projects
  * Certifications
  * Achievements
  * Languages
  * Professional Summary
* 💡 Generate resume improvement suggestions.
* ❓ Generate five interview questions based on the resume.
* 💬 Chat with your resume using Retrieval-Augmented Generation (RAG).
* ⚡ Fast semantic search using Chroma Vector Database.
* 🎨 Simple and interactive Streamlit interface.

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Frameworks & Libraries

* Streamlit
* LangChain
* ChromaDB
* Mistral AI
* Pydantic
* python-dotenv

### AI & RAG Components

* Mistral Large (LLM)
* Mistral Embeddings
* RecursiveCharacterTextSplitter
* TextLoader
* Chroma Vector Store
* Maximum Marginal Relevance (MMR) Retrieval

---

## 📂 Project Structure

```text
resume_analyzer/
│
├── app.py                 # Streamlit UI
├── rag.py                 # RAG pipeline
├── requirements.txt
├── .env
├── README.md
└── sample_resume.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git

cd resume-analyzer
```

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
MISTRAL_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📋 How It Works

1. Upload a resume in **TXT** format.
2. The resume is loaded using LangChain's `TextLoader`.
3. The text is split into smaller chunks using `RecursiveCharacterTextSplitter`.
4. Each chunk is converted into vector embeddings using **Mistral Embeddings**.
5. The embeddings are stored in **ChromaDB**.
6. Relevant chunks are retrieved using **Maximum Marginal Relevance (MMR)**.
7. Mistral Large analyzes the retrieved content.
8. Structured resume information is generated using a **Pydantic Output Parser**.
9. Users can ask questions about the uploaded resume through the chat interface.

---

## 🧠 RAG Pipeline

```text
Resume (.txt)
        │
        ▼
Text Loader
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
Retriever (MMR)
        │
        ▼
Mistral Large LLM
        │
        ▼
Structured Resume Analysis
        │
        ▼
Resume Q&A
```

---

## 📷 Application Features

* Resume Upload
* AI Resume Analysis
* Resume Summary
* Resume Improvement Suggestions
* Interview Question Generation
* Resume Chat Assistant

---

## 🚀 Future Improvements

* Support PDF resumes.
* Support DOCX resumes.
* Export analysis as PDF.
* Resume scoring system.
* ATS compatibility score.
* Keyword matching for job descriptions.
* Cover letter generation.
* Multi-language resume support.
* Conversation history.
* Multiple resume comparison.

---

## 📦 Requirements

* Python 3.10+
* Streamlit
* LangChain
* langchain-mistralai
* chromadb
* python-dotenv
* pydantic

---

## 👨‍💻 Author

**Anuj Shrestha**

GitHub: https://github.com/AnujrajShrestha

---

## 📄 License

This project is licensed under the MIT License.

Feel free to fork, modify, and improve the project.
