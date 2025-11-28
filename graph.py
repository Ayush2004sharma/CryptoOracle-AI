# graph.py
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from agents.news_agent import create_crypto_news_analyst
from agents.fundamental_analysis_agent import create_fundamentals_analyst
from agents.technical_anlyst_agent import create_technical_analyst
from agents.social_media_agent import create_sentiment_analyst
from agents.research_analyst_agent import create_research_analyst_agent
from agents.risk_management_agent import create_risk_manager_agent
from toolkit.crypto_toolkit import MyCryptoToolKit
from dotenv import load_dotenv
import os

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

# 🔐 API KEYS (Now loaded from .env)
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
CRYPTOPANIC_KEY = os.getenv("CRYPTO_PANIC_KEY")
COINGECKO_KEY = os.getenv("COINGECKO_API_KEY")

# -------------------------------
# 🤖 Initialize LLM (Gemini)
# -------------------------------
from langchain_google_genai import ChatGoogleGenerativeAI

if not GEMINI_KEY:
    raise ValueError("❌ Missing GOOGLE_API_KEY in .env file!")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

# -------------------------------
# 🧰 Initialize Toolkit
# -------------------------------
toolkit = MyCryptoToolKit(
    cryptopanic_key=CRYPTOPANIC_KEY,
    coingecko_key=COINGECKO_KEY,
)

# -------------------------------
# 🧠 State Model
# -------------------------------
class AgentState(TypedDict):
    coin: str
    trade_date: str
    user_type: str
    horizon: str
    messages: List[BaseMessage]
    news_report: Optional[str]
    fundamentals_report: Optional[str]
    technical_report: Optional[str]
    sentiment_report: Optional[str]
    research_summary: Optional[str]
    research_decision: Optional[str]
    research_confidence: Optional[float]
    risk_notes: Optional[str]
    horizon: Optional[dict]
    final_reason: Optional[str]
    confidence: Optional[float]
    final_recommendation: Optional[str]


# -------------------------------
# 🔄 AGENT NODES
# -------------------------------
def news_node(state):
    state["messages"] = [
        HumanMessage(content=f"Analyze recent news for {state['coin']}.")
    ]
    return create_crypto_news_analyst(llm, toolkit)(state)


def fundamentals_node(state):
    state["messages"] = [
        HumanMessage(content=f"Analyze fundamentals for {state['coin']}.")
    ]
    return create_fundamentals_analyst(llm, toolkit)(state)


def technical_node(state):
    state["messages"] = [
        HumanMessage(content=f"Analyze technical indicators for {state['coin']}.")
    ]
    return create_technical_analyst(llm, toolkit)(state)


def sentiment_node(state):
    state["messages"] = [
        HumanMessage(content=f"Analyze social sentiment for {state['coin']}.")
    ]
    return create_sentiment_analyst(llm, toolkit)(state)


def research_node(state):
    state["messages"] = [
        HumanMessage(
            content=f"Create a consolidated research summary for {state['coin']}."
        )
    ]
    return create_research_analyst_agent(llm)(state)


def risk_node(state):
    state["messages"] = [
        HumanMessage(content=f"Assess risk for {state['coin']}.")
    ]
    return create_risk_manager_agent(llm)(state)


# -------------------------------
# 🧩 Build Complete Workflow
# -------------------------------
def trading_graph(llm, toolkit):
    workflow = StateGraph(AgentState)

    workflow.add_node("news", news_node)
    workflow.add_node("fundamentals", fundamentals_node)
    workflow.add_node("technical", technical_node)
    workflow.add_node("sentiment", sentiment_node)
    workflow.add_node("research", research_node)
    workflow.add_node("risk", risk_node)

    workflow.add_edge("news", "fundamentals")
    workflow.add_edge("fundamentals", "technical")
    workflow.add_edge("technical", "sentiment")
    workflow.add_edge("sentiment", "research")
    workflow.add_edge("research", "risk")
    workflow.add_edge("risk", END)

    workflow.set_entry_point("news")
    return workflow.compile()


graph = trading_graph(llm, toolkit)
