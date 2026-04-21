"""
Lightweight retriever for memory-constrained deployments (e.g. Render free tier).
Uses sklearn TF-IDF instead of FAISS + sentence-transformers (no PyTorch needed).
The full FAISS-based retriever lives in retriever.py and is used in local/full deployments.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

FINANCE_KNOWLEDGE = [
    "An emergency fund should cover 3-6 months of living expenses.",
    "The 50/30/20 rule: 50% needs, 30% wants, 20% savings.",
    "High interest debt like credit cards should be paid off first.",
    "Index funds are low-cost investments that track market performance.",
    "Diversification reduces investment risk by spreading across asset classes.",
    "A budget helps track income and expenses to achieve financial goals.",
    "Compound interest grows wealth significantly over long time periods.",
    "Term life insurance is generally more cost-effective than whole life.",
    "Tax-advantaged accounts like 401k and IRA reduce taxable income.",
    "Avoid lifestyle inflation — increase savings as income grows.",
    "The debt snowball method pays off smallest debts first for psychological wins.",
    "The debt avalanche method pays off highest interest debt first to save money.",
    "A net worth statement lists all assets minus all liabilities.",
    "Dollar cost averaging reduces risk by investing fixed amounts regularly.",
    "An HSA (Health Savings Account) offers triple tax advantages for medical costs.",
    "Roth IRA contributions are made after-tax but withdrawals in retirement are tax-free.",
    "Credit score is affected by payment history, utilization, and account age.",
    "Keeping credit utilization below 30% helps maintain a good credit score.",
    "Rebalancing a portfolio annually keeps your risk level aligned with your goals.",
    "Inflation erodes purchasing power — investments should outpace inflation over time.",
]

_vectorizer = None
_matrix = None

def _build_index():
    global _vectorizer, _matrix
    _vectorizer = TfidfVectorizer()
    _matrix = _vectorizer.fit_transform(FINANCE_KNOWLEDGE)

def retrieve_context(query: str, k: int = 3) -> str:
    if _vectorizer is None:
        _build_index()
    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _matrix)[0]
    top_k = np.argsort(scores)[::-1][:k]
    return "\n".join(FINANCE_KNOWLEDGE[i] for i in top_k)
