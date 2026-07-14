# 📂 AI Project Analyzer

An AI-powered project analysis tool built with **LangChain**, **Mistral AI**, **ChromaDB**, and **Streamlit**. Upload an entire software project (ZIP file), and the application automatically analyzes the codebase, generates a technical summary, provides architectural suggestions, and allows you to chat with your project using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📁 Upload an entire project as a ZIP file
- 🔍 Automatically scans source code files
- 🧠 Generates vector embeddings using Mistral Embeddings
- 💾 Stores project knowledge in ChromaDB
- 📄 Produces a structured project analysis including:
  - Project Name
  - File List
  - Project Summary
  - Improvement Suggestions
- 💬 Chat with your project using natural language
- ⚡ Uses MMR retrieval for better context selection
- 🌐 Interactive Streamlit interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- ChromaDB
- Pydantic
- python-dotenv

---

## 📁 Project Structure

```
project-analyzer/
│
├── app.py                 # Streamlit UI
├── main.py                # CLI version
├── db.py                  # Builds vector database
├── analyzer_db/           # Chroma vector database
├── requirements.txt
├── .env
└── README.md
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/project-analyzer.git

cd project-analyzer
```

---

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

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create a `.env` file

```env
MISTRAL_API_KEY=your_api_key
```

---

## ▶️ Running the Application

### Streamlit UI

```bash
streamlit run app.py
```

---

### CLI Version

First create the vector database

```bash
python db.py
```

Then run

```bash
python main.py
```

---

## 📂 Supported File Types

The analyzer currently supports:

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- React (.jsx, .tsx)
- HTML
- CSS
- JSON
- Markdown
- TXT
- PHP
- C
- C++
- Java

More file extensions can easily be added.

---

## ⚙️ How It Works

### Step 1

Upload a project ZIP file.

↓

### Step 2

Extract project files.

↓

### Step 3

Load source files using `DirectoryLoader`.

↓

### Step 4

Split documents into chunks.

↓

### Step 5

Generate embeddings with Mistral Embeddings.

↓

### Step 6

Store vectors inside ChromaDB.

↓

### Step 7

Retrieve relevant code using MMR Retrieval.

↓

### Step 8

Generate:

- Technical Summary
- Project Information
- Engineering Suggestions

↓

### Step 9

Chat with your codebase using RAG.

---

## 📊 Analysis Output

The application generates a structured report containing:

- Project Name
- File List
- Project Path
- Technical Summary
- Improvement Suggestions

Example:

```
Project Name:
Portfolio Website

Files:
- app.py
- utils.py
- requirements.txt
- README.md

Summary:
A Streamlit-based application that indexes project files using ChromaDB and enables AI-powered project analysis through Retrieval-Augmented Generation.

Suggestions:
- Add logging
- Improve exception handling
- Ignore virtual environments during indexing
- Add unit tests
```

---

## 💬 Example Questions

You can ask questions like:

- Explain the project architecture.
- How does authentication work?
- Which files handle database operations?
- Where is the API implemented?
- What improvements would you recommend?
- Explain this function.
- Summarize the backend.
- Which modules are interconnected?
- Are there any security issues?
- Which file should I modify to add a new feature?

---

## 📈 Future Improvements

- 📄 PDF report generation
- 📁 Folder upload without ZIP (desktop support)
- 📊 Project statistics dashboard
- 🏗️ Architecture diagram generation
- 🐞 Bug detection
- 🔒 Security vulnerability analysis
- ⚡ Multi-language support
- 🌳 Interactive project tree
- 🔍 Semantic code search
- 🤖 Multi-agent analysis

---

## 👨‍💻 Author

Developed by Anujraj Shrestha

---

## 📜 License

This project is licensed under the MIT License.
