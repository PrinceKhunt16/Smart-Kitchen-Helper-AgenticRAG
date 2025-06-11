from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from .recipe_agent import recipe_agent
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Dict[str, str]]

@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.question
    chat_history = request.chat_history[-6:]

    initial_state = {
        "query": query,
        "chat_history": chat_history,
        "context": "",
        "answer": "",
        "context_found": False
    }
    
    final_state = recipe_agent.invoke(initial_state)

    return {"answer": final_state["answer"]}