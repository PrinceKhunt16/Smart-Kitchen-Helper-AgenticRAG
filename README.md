# 🧠 Smart Kitchen Helper — Cooking Assistant with RAG + Agent Search

## **Previews**
![1](previews/ss1.png)
![2](previews/ss2.png)
![3](previews/ss3.png)

---

## 🔧 Tech Stack

- **LLM Provider**: [GroqCloud](https://console.groq.com/) with open-source models (Mistral/Samba)
- **Frameworks**: 
  - [LangGraph](https://docs.langchain.com/langgraph/) for building multi-step agent logic
  - [LangChain](https://www.langchain.com/) for document processing and RAG
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Vector Store**: ChromaDB
- **Search Tool**: DuckDuckGo

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-kitchen-helper.git
   cd smart-kitchen-helper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```  

## 🔥 Start the Application

Run the Streamlit frontend:
```bash
streamlit run frontend/app.py