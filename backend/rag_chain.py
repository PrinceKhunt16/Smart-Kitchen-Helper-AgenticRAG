from .chroma_setup import get_chroma
from .groq_client import get_groq_client

def rag_chain(query: str, chat_history: list):
    chroma = get_chroma()

    results_with_scores = chroma.similarity_search_with_score(query, k=3)
    
    RELEVANCE_THRESHOLD = 1 
    
    relevant_docs = []

    for doc, score in results_with_scores:
        print(f"Document score: {score}") 
        if score < RELEVANCE_THRESHOLD: 
            relevant_docs.append(doc)
    
    print(f"Found {len(relevant_docs)} relevant documents out of {len(results_with_scores)}")
    
    if not relevant_docs:
        print("No relevant documents found - will trigger fallback search")
        return "", False

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    conversation_history = ""

    for entry in chat_history:
        role = "User" if entry["role"] == "user" else "Assistant"
        conversation_history += f"{role}: {entry['content']}\n"

    prompt = (
        f"Here are some recipe details:\n{context}\n\n"
        f"Conversation so far:\n{conversation_history}\n"
        f"User: {query}\n\n"
        f"Based on the above recipes and conversation, provide a helpful cooking answer. "
        f"If the recipe information doesn't contain relevant details for the user's question, "
        f"say 'I don't have specific information about that in my recipe database.'"
    )

    groq_client = get_groq_client()

    response = groq_client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": "You are a helpful cooking assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    return response.choices[0].message.content, True