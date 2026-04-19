import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
]

_vectorizer = TfidfVectorizer()
_matrix = _vectorizer.fit_transform(FINANCE_KNOWLEDGE)

def retrieve_context(query: str, k: int = 3) -> str:
    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _matrix)[0]
    top_k = np.argsort(scores)[-k:][::-1]
    return "\n".join(FINANCE_KNOWLEDGE[i] for i in top_k)
