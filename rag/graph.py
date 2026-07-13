import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages

load_dotenv()

llm = ChatOpenRouter(model="tencent/hy3:free")


def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
graph = graph.compile()

question = "hi"

for event in graph.stream(MessagesState({"messages": [HumanMessage(question)]})):
    for value in event.values():
        print("Assistant:", value["messages"][-1].content)
