from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.graph import END, StateGraph 
from langchain_core.runnables import RunnableLambda
from .rag_chain import rag_chain
from .groq_client import get_groq_client
from typing import TypedDict

search_tool = DuckDuckGoSearchResults()

class RecipeAgentState(TypedDict):
    query: str
    chat_history: list
    context: str
    answer: str
    context_found: bool

def rag_chain_node(state: RecipeAgentState) -> RecipeAgentState:
    print("🔎 Running RAG chain...")
    answer, context_found = rag_chain(state["query"], state["chat_history"])
    
    return {
        **state,
        "answer": answer,
        "context_found": context_found
    }

def search_agent_node(state: RecipeAgentState) -> RecipeAgentState:
    print("🌐 No context from RAG. Using fallback search...")

    search_results = search_tool.run(state["query"])
    print("Search results:", search_results)

    search_prompt = (
        f"Here are some additional cooking details:\n{search_results}\n\n"
        f"Conversation so far:\n{state['chat_history']}\n"
        f"User: {state['query']}\n\n"
        f"IMPORTANT: If the user's question is not related to cooking or recipes, "
        f"respond politely saying that this chatbot only handles recipe-related questions. "
        f"Otherwise, provide a helpful cooking answer based on the context."
    )
    groq_client = get_groq_client()

    response = groq_client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": "You are a helpful cooking assistant."},
            {"role": "user", "content": search_prompt}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    return {
        **state,
        "answer": response.choices[0].message.content,
        "context_found": True
    }

graph = StateGraph(RecipeAgentState)

graph.add_node("rag_chain", RunnableLambda(rag_chain_node))
graph.add_node("search_agent", RunnableLambda(search_agent_node))

def decide_next_node(state: RecipeAgentState) -> str:
    if state["context_found"]:
        return END
    else:
        return "search_agent"

graph.set_entry_point("rag_chain")
graph.add_conditional_edges("rag_chain", decide_next_node)
graph.add_edge("search_agent", END)

recipe_agent = graph.compile()