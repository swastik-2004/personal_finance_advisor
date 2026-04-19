from typing import TypedDict
from langgraph.graph import StateGraph, END
from rag.retriever import retrieve_context
from rag.chatbot import ask_chatbot

class ChatState(TypedDict):
    query: str
    context: str
    transactions: list[dict]
    response: str

def retrieve_node(state: ChatState) -> ChatState:
    state["context"] = retrieve_context(state["query"])
    return state

def respond_node(state: ChatState) -> ChatState:
    state["response"] = ask_chatbot(state["query"], state["transactions"])
    return state

def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("respond", respond_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", END)
    return graph.compile()

finance_graph = build_graph()

def run_chat(query: str, transactions: list[dict] = []) -> str:
    result = finance_graph.invoke({
        "query": query,
        "context": "",
        "transactions": transactions,
        "response": ""
    })
    return result["response"]
