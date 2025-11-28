# main.py

from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from toolkit.crypto_toolkit import MyCryptoToolKit
from agents.news_agent import create_crypto_news_analyst
from agents.fundamental_analysis_agent import create_fundamentals_analyst
from agents.technical_anlyst_agent import create_technical_analyst
from agents.social_media_agent import create_sentiment_analyst
from langchain_groq import ChatGroq
import os
# ----------------------------------------------------
# 🔐 LOAD ENV VARIABLES
# ----------------------------------------------------
load_dotenv()

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
CRYPTOPANIC_KEY = os.getenv("CRYPTO_PANIC_KEY")
COINGECKO_KEY = os.getenv("COINGECKO_API_KEY")

# ----------------------------------------------------
# 🤖 LLM (Gemini)
# ----------------------------------------------------

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)


# ----------------------------------------------------
# 🛠 TOOLKIT (News, Fundamentals, Technicals, Social Sentiment)
# ----------------------------------------------------
toolkit = MyCryptoToolKit(
    cryptopanic_key=CRYPTOPANIC_KEY,
    coingecko_key=COINGECKO_KEY,
)

# ----------------------------------------------------
# 📦 SHARED STATE
# ----------------------------------------------------
state = {
    "coin": "bitcoin",
    "company_of_interest": "bitcoin",
    "trade_date": "2025-07-25",
    "messages": [HumanMessage(content="Analyze this bitcoin.")],
}

# ----------------------------------------------------
# 🧠 RUN ANALYSIS
# ----------------------------------------------------

## SENTIMENT ANALYSIS
print("\n🔍 Running Sentiment Analyst...")
sentiment_agent = create_sentiment_analyst(llm, toolkit)
sent_result = sentiment_agent(state)
print("\n💬 SENTIMENT REPORT:\n", sent_result["sentiment_report"])
