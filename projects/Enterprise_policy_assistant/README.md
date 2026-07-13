# 🏢 Enterprise Policy Assistant (RAG)

A Retrieval-Augmented Generation (RAG) application that enables employees to ask questions about company policies using natural language. The assistant retrieves relevant information from a company policy PDF using a vector database and generates accurate responses with Mistral AI.

## ✨ Features

* 📄 Load and process company policy documents (PDF)
* ✂️ Split documents into semantic chunks
* 🔍 Store embeddings in a Chroma vector database
* 🧠 Retrieve the most relevant document sections using MMR (Maximal Marginal Relevance)
* 🤖 Generate answers using Mistral Large Language Model
* 💬 Interactive Streamlit chat interface
* ⚡ Cached model loading for improved performance
* 📚 Displays retrieved document context for transparency

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Mistral AI
* Chroma Vector Database
* PyPDFLoader
* RecursiveCharacterTextSplitter
* python-dotenv

---

## 📂 Project Structure

```text
Enterprise_policy_assistant/
│
├── app.py                              # Streamlit application
├── db.py                               # Creates the Chroma vector database
├── main.py                             # Command-line version
├── Company_Policy_RAG_Assistant.pdf    # Company policy document
├── Entreprise_db/                      # Persistent Chroma database
├── .env                                # API keys
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Enterprise_policy_assistant
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
MISTRAL_API_KEY=your_mistral_api_key
```

---

## 📄 Create the Vector Database

Place your company policy PDF in the project folder and run:

```bash
python db.py
```

This script will:

* Load the PDF document
* Split it into chunks
* Generate embeddings
* Store them in the `Entreprise_db` directory

---

## 🚀 Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 💻 Run the Command-Line Version

```bash
python main.py
```

---

## 🔄 RAG Workflow

1. Load the company policy PDF.
2. Split the document into smaller chunks.
3. Generate embeddings using Mistral Embeddings.
4. Store embeddings in Chroma.
5. Convert the user's question into an embedding.
6. Retrieve the most relevant document chunks using MMR.
7. Send the retrieved context and question to the Mistral LLM.
8. Generate an answer based only on the retrieved context.
9. Display the response to the user.

---

## 📦 Main Libraries

* langchain
* langchain-community
* langchain-mistralai
* chromadb
* streamlit
* python-dotenv
* pypdf

---

## 📸 Application

The application provides:

* Chat-based interface
* Persistent chat history
* Company policy question answering
* Context retrieval
* Fast responses through cached resources

---

## 📌 Example Questions

* What is the company's purpose and scope?
* What is the leave policy?
* What are the working hours?
* What is the code of conduct?
* What are the employee responsibilities?
* What happens in case of a policy violation?

---

## 📖 How It Works

When a user asks a question:

1. The question is embedded using the Mistral embedding model.
2. Chroma retrieves the most relevant sections of the policy document.
3. The retrieved context is passed to the Mistral Large language model.
4. The model generates an answer strictly based on the retrieved information.
5. If the answer is not available in the document, the assistant replies:

> "I could not find the answer in the document."

---

## 👨‍💻 Author

**Anuj**

A GenAI and Python developer exploring Retrieval-Augmented Generation (RAG), LangChain, and Large Language Models to build practical AI applications.

---

## 📄 License

This project is intended for educational and learning purposes. Feel free to modify and extend it for your own projects.
