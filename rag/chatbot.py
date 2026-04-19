from groq import Groq
from app.core.config import settings
from rag.retriever import retrieve_context

client = Groq(api_key=settings.groq_api_key)

def ask_chatbot(query: str, user_transactions: list[dict] = []) -> str:
    context = retrieve_context(query)

    transaction_summary = ""
    if user_transactions:
        total = sum(t["amount"] for t in user_transactions)
        by_category: dict[str, float] = {}
        for t in user_transactions:
            cat = t.get("category") or "Other"
            by_category[cat] = by_category.get(cat, 0) + t["amount"]
        breakdown = ", ".join(f"{cat}: ${amt:.2f}" for cat, amt in by_category.items())
        transaction_summary = f"\nUser's total spending: ${total:.2f}\nBreakdown by category: {breakdown}"

    prompt = f"""You are a personal finance advisor. Use the context below to answer the user's question.

Context:
{context}
{transaction_summary}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
    )
    return response.choices[0].message.content
