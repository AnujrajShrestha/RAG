# 📄 Research Paper Summarizer & Chat (RAG)

A Streamlit-based AI application that allows users to upload a research paper (PDF), automatically generates a concise summary, and enables interactive question-answering using Retrieval-Augmented Generation (RAG).

The application uses **LangChain**, **Mistral AI**, and **ChromaDB** to retrieve relevant sections of the uploaded document and answer user queries accurately.

---

## 🚀 Features

* 📤 Upload any research paper in PDF format
* ✂️ Automatically split the document into semantic chunks
* 🧠 Generate vector embeddings using Mistral Embeddings
* 💾 Store document embeddings in Chroma Vector Database
* 📝 Generate an AI-powered summary of the research paper
* 💬 Chat with the uploaded research paper using RAG
* 🔍 Retrieve only the most relevant document chunks for each query
* ⚡ Simple and interactive Streamlit interface

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Mistral AI
* ChromaDB
* PyPDF
* Python Dotenv

---

## 📂 Project Structure

```text
researchPaper_summarizer/
│
├── app.py                  # Streamlit application
├── requirements.txt        # Project dependencies
├── .env                    # API keys
├── README.md
└── temp/                   # Temporary uploaded PDFs
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd researchPaper_summarizer
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

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

The application will open automatically in your browser.

---

## 🔄 Workflow

```text
Upload PDF
      │
      ▼
Load PDF
      │
      ▼
Split into Chunks
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Generate Summary
      │
      ▼
Chat with the Research Paper
```

---

## 📚 How It Works

1. The user uploads a research paper in PDF format.
2. The document is loaded using `PyPDFLoader`.
3. The text is divided into overlapping chunks using `RecursiveCharacterTextSplitter`.
4. Each chunk is converted into embeddings using the **Mistral Embed** model.
5. The embeddings are stored in a Chroma vector database.
6. During summarization or question answering, the retriever fetches the most relevant chunks.
7. These chunks are passed to the Mistral Large language model, which generates context-aware responses.

---

## 📦 Dependencies

* streamlit
* langchain
* langchain-community
* langchain-core
* langchain-text-splitters
* langchain-mistralai
* chromadb
* pypdf
* python-dotenv

---

## 🎯 Future Improvements

* Support multiple PDF uploads
* Persistent vector database
* Citation and source highlighting
* Conversation memory
* Export summaries as PDF or DOCX
* Adjustable summary length
* Research paper metadata extraction (title, authors, abstract)
* Dark mode UI
* Multi-language support

---

## 📸 Application Features

* Upload a research paper
* AI-generated research summary
* Interactive chat interface
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed as a **Generative AI & RAG** project using **Streamlit**, **LangChain**, **Mistral AI**, and **ChromaDB**.
