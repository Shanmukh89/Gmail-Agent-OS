from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
import os
import json
from schemas import EmailCreate

# Define the state for the LangGraph
class AgentState(TypedDict):
    email: dict
    categories: list
    classification_result: dict
    confidence: int
    needs_review: bool
    notified: bool

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def preprocess_node(state: AgentState):
    # In a real app, clean HTML, extract text, etc.
    email_data = state["email"]
    snippet = email_data.get("snippet", "")
    subject = email_data.get("subject", "")
    sender = email_data.get("sender", "")
    return state

def classify_node(state: AgentState):
    categories = state["categories"]
    email_data = state["email"]
    
    cat_descriptions = "\n".join([f"- {c.name}: {c.description}" for c in categories])
    
    prompt = f"""
    You are an intelligent email routing assistant.
    Classify the following email into one of the user's categories.
    
    Categories:
    {cat_descriptions}
    
    Email:
    Sender: {email_data.get('sender')}
    Subject: {email_data.get('subject')}
    Snippet: {email_data.get('snippet')}
    
    Respond in JSON format:
    {{"category_name": "Name", "confidence": 0-100}}
    """
    
    messages = [SystemMessage(content=prompt)]
    response = llm.invoke(messages)
    
    try:
        result = json.loads(response.content)
        return {"classification_result": result, "confidence": result.get("confidence", 0)}
    except json.JSONDecodeError:
        return {"classification_result": {"category_name": "Uncategorized"}, "confidence": 0}

def confidence_check_node(state: AgentState):
    confidence = state.get("confidence", 0)
    needs_review = confidence < 80
    return {"needs_review": needs_review}

def notification_decision_node(state: AgentState):
    cat_name = state["classification_result"].get("category_name")
    categories = state["categories"]
    
    notify = False
    for c in categories:
        if c.name.lower() == cat_name.lower() and c.notify:
            notify = True
            break
            
    return {"notified": notify}

def apply_label_node(state: AgentState):
    # Here we would update the DB and potentially Gmail API
    # Returning final state
    return state

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("preprocess", preprocess_node)
workflow.add_node("classify", classify_node)
workflow.add_node("confidence_check", confidence_check_node)
workflow.add_node("notification_decision", notification_decision_node)
workflow.add_node("apply_label", apply_label_node)

workflow.set_entry_point("preprocess")
workflow.add_edge("preprocess", "classify")
workflow.add_edge("classify", "confidence_check")
workflow.add_edge("confidence_check", "notification_decision")
workflow.add_edge("notification_decision", "apply_label")
workflow.add_edge("apply_label", END)

app = workflow.compile()

def process_email_pipeline(email_data: dict, categories: list):
    initial_state = {
        "email": email_data,
        "categories": categories,
        "classification_result": {},
        "confidence": 0,
        "needs_review": False,
        "notified": False
    }
    
    final_state = app.invoke(initial_state)
    return final_state
