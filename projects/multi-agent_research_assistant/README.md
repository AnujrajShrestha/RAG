# 🔎 Multi-Agent Research Assistant

A **Multi-Agent AI Research Assistant** built with **LangChain, Groq, Tavily Search, BeautifulSoup, and Streamlit**.

The application uses multiple AI agents to automatically search the web, extract relevant information, generate a detailed research report, and review the quality of the report.

---

## 📌 Features

- 🌐 Searches the web for recent and reliable information using Tavily
- 📖 Scrapes the most relevant webpage for detailed content
- ✍️ Generates a structured research report
- 🧐 Critiques the generated report with strengths, weaknesses, and score
- 💻 Beautiful Streamlit interface
- 📥 Download reports as Markdown
- 📜 Stores previous research sessions during runtime

---

## 🛠️ Tech Stack

- Python
- LangChain
- Groq LLM
- Tavily Search API
- BeautifulSoup4
- Requests
- Streamlit
- Rich
- Python Dotenv

---

## 📂 Project Structure

```
multi-agent-research-assistant/
│
├── app.py                 # Streamlit application
├── pipeline.py            # Research pipeline
├── agents.py              # AI agents
├── tools.py               # Search & scraping tools
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ How It Works

The application follows a **4-Agent workflow**.

```
          User Topic
               │
               ▼
     🔍 Search Agent
               │
               ▼
      📖 Reader Agent
               │
               ▼
      ✍️ Writer Agent
               │
               ▼
      🧐 Critic Agent
               │
               ▼
        Final Report
```

### 1. Search Agent

- Uses Tavily Search API
- Finds recent and reliable resources
- Returns:
  - Titles
  - URLs
  - Snippets

---

### 2. Reader Agent

- Selects the most relevant URL
- Scrapes webpage content
- Removes unnecessary HTML elements
- Returns clean text

---

### 3. Writer Agent

Generates a professional research report containing:

- Introduction
- Key Findings
- Conclusion
- Sources

---

### 4. Critic Agent

Evaluates the report and provides:

- Overall score
- Strengths
- Weaknesses
- Improvement suggestions
- Final verdict

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/your-username/multi-agent-research-assistant.git

cd multi-agent-research-assistant
```

---

### Create a virtual environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 💡 Example

Research Topic

```
Impact of Artificial Intelligence on Healthcare
```

Pipeline Output

```
Search Agent
      ↓
Reader Agent
      ↓
Writer Agent
      ↓
Critic Agent
      ↓
Final Research Report
```

---

## 📸 User Interface

The Streamlit interface includes:

- Research topic input
- Live pipeline progress
- Final report
- Critic feedback
- Intermediate agent outputs
- Download report button
- Previous research history

---

## 📄 Report Structure

The generated report follows this format:

```
Introduction

Key Findings

1.
2.
3.

Conclusion

Sources
```

---

## 📦 Dependencies

- langchain
- langchain-groq
- tavily-python
- streamlit
- beautifulsoup4
- requests
- python-dotenv
- rich

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🎯 Learning Objectives

This project demonstrates:

- Multi-Agent AI workflows
- LangChain Agents
- Tool Calling
- Web Search Integration
- Web Scraping
- Prompt Engineering
- LLM Pipelines
- Report Generation
- Streamlit Deployment

---

## 🔮 Future Improvements

- Support multiple URLs instead of one
- Add PDF report export
- Save research history in a database
- Citation formatting (APA/MLA)
- Multi-language support
- Streaming responses
- LangGraph implementation
- Source ranking based on credibility
- Image extraction from articles
- Follow-up research chat

---

## 👨‍💻 Author

**Anuj Shrestha**

- GitHub: https://github.com/AnujrajShrestha

---

## ⭐ If you found this project helpful, consider giving it a star on GitHub!