import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")

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

def build_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    docs = [Document(page_content=text) for text in FINANCE_KNOWLEDGE]
    store = FAISS.from_documents(docs, embeddings)
    store.save_local(VECTOR_STORE_PATH)
    print("Vector store built and saved.")

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

if __name__ == "__main__":
    build_vector_store()
