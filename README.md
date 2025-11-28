# 📊 CryptoOracle – AI-Powered Crypto Investment Assistant

CryptoOracle is a multi-agent AI system designed to help crypto investors make confident and informed decisions.  
It combines **news analysis, fundamentals, technical indicators, and market sentiment** into a single, easy-to-understand investment verdict.

Built using **LangGraph, LangChain, Python, and Streamlit**, CryptoOracle delivers AI-generated insights through a clean and interactive dashboard.

---

## 🚀 Features

### 🤖 Multi-Agent AI System

* **News Analyst** → Fetches verified crypto-related news and major macro signals.  
* **Fundamental Analyst** → Evaluates supply, liquidity, issuance, and ecosystem activity.  
* **Technical Analyst** → Computes RSI, MACD, Bollinger Bands, and trend strength.  
* **Sentiment Analyst** → Uses Fear & Greed Index + news sentiment to estimate market psychology.  
* **Research Analyst** → Summarizes all findings into a clear human-style narrative.  
* **Risk Management Analyst** → Aligns the final recommendation with investor risk profile and time horizon.

---

### 🖥️ User-Friendly Dashboard (Streamlit)

* Choose cryptocurrency  
* Select investor profile (New / Existing)  
* Select investment duration (Short / Medium / Long term)  
* Receive final output:

Recommendation → Buy / Hold / Sell
Confidence Score → e.g., 0.72
Time Horizon → Based on your selection


Includes detailed tabs:

- 📰 News  
- 📊 Fundamentals  
- 📈 Technical Analysis  
- 💬 Market Sentiment  
- 📚 Final Summary  

---

### 🔗 APIs & Tools Integrated

| Component | Provider |
|----------|----------|
| Fundamentals & Price Data | CoinGecko API |
| News Intelligence | Tavily Search API |
| Market Sentiment | Fear & Greed Index API |
| TA Indicators | Pandas-TA |
| AI Reasoning | LangChain + LangGraph |

> ❗ Reddit functionality has been removed — no authentication is required.

---

## 🖥️ Example Input

Cryptocurrency → Bitcoin
Investor Type → New Buyer
Investment Duration → Short Term (1–3 months)


---

## 🧠 Sample AI Verdict

CryptoOracle Verdict for Bitcoin
✔ Recommendation: HOLD
📈 Confidence Score: 0.70
⏳ Timeframe: Short Term

💡 Reasoning:

Technical momentum is uncertain.

Sentiment recovering but cautious.

Fundamentals remain strong for long-term outlook.


---

## ⚙️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **LangGraph**
- **Pandas-TA**
- **Tavily API**
- **CoinGecko API**

---

## 🏗️ Project Structure



├── agents/
│ ├── news_agent.py
│ ├── fundamental_agent.py
│ ├── technical_agent.py
│ ├── sentiment_agent.py
│
├── toolkit/
│ ├── crypto_toolkit.py
│ ├── crypto_tools_wrapped.py
│ ├── sentiment.py # Market sentiment module (Fear & Greed)
│
├── app.py
├── graph.py
├── README.md
└── requirements.txt


---

## 🛠️ Setup & Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YourUsername/CryptoOracle.git
cd CryptoOracle

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Create .env File
COINGECKO_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

4️⃣ Run the Application
streamlit run app.py

📌 Future Enhancements

Add Twitter/X sentiment scoring

Support portfolio tracking and alerts

Expand to DeFi protocols and L2 ecosystems

Add multilingual support
