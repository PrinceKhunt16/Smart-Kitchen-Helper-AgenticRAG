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

---

## 🌟 Features

- Upload your own recipe documents
- Ask cooking-related questions via chat interface
- Uses vector embeddings to find relevant answers from uploaded docs
- Falls back to a web search agent when no relevant local data is found
- Smart prompt logic to restrict responses only to cooking-related queries