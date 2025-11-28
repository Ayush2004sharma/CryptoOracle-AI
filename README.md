# 📊 NeutroFi – AI-Powered Crypto Investment Assistant

NeutroFi is a multi-agent AI system that helps crypto investors make smarter decisions.
It combines **news analysis, fundamentals, technical indicators, and community sentiment** into a clear, plain-English investment verdict.

Built using **LangGraph, LangChain, Python, and Streamlit**, NeutroFi provides both **AI-powered insights** and an easy-to-use **dashboard** for investors.

---

## 🚀 Features

✅ **Multi-Agent AI System**

* **News Analyst** → Fetches credible crypto news & flags regulatory/macro risks.
* **Fundamental Analyst** → Analyzes supply, issuance, liquidity, and developer activity.
* **Technical Analyst** → Computes RSI, MACD, Bollinger Bands.
* **Sentiment Analyst** → Filters Reddit chatter into usable community signals.
* **Research Analyst** → Summarizes all agent insights into one clear view.
* **Risk Management Analyst** → Matches results with the user’s risk appetite & timeframe.

✅ **User-Friendly Dashboard** (Streamlit)

* Select your **coin**, **buyer type (new/existing)**, and **investment duration**.
* Get a **final recommendation** (`Buy`, `Hold`, or `Sell`) with **confidence score**.
* Explore details via tabs: **News, Fundamentals, Technical, Sentiment, Overall Summary**.

✅ **APIs & Tools Integrated**

* CoinGecko (fundamentals & price data)
* CryptoPanic, Google News, Reddit (news & sentiment)
* Pandas-TA (technical indicators)
* LangGraph (multi-agent workflow orchestration)

---

## 🖥️ User Flow

### 1. Input Preferences

User selects:

* Cryptocurrency (e.g., Bitcoin, Ethereum, Solana)
* Buyer Type (New / Existing)
* Investment Duration (Short, Medium, Long term)

📸 *Sample Input Screen:*

```
What cryptocurrency are you interested in today? → Bitcoin  
What describes you best? → New Buyer  
Investment Duration → Short term (1-3 months)  
```

### 2. AI Verdict Screen

* **Final Recommendation** → Buy / Hold / Sell
* **Confidence Score** → e.g. 0.70
* **Timeframe** → Matches selected duration
* **Reason** → Plain-English explanation

📸 *Sample Verdict:*

```
Neu’s Verdict for Bitcoin
✅ Final Recommendation: Hold
📈 Confidence Score: 0.70
⏳ Timeframe: Short term (1–3 months)
💡 Reason: New entry not advised unless confidence and long-term view are strong.
```

### 3. Detailed Reports

Tabs provide deeper insights:

* **News** → Summarized headlines + sentiment score.
* **Fundamentals** → Supply, liquidity, issuance, developer activity.
* **Technical** → RSI, MACD, Bollinger Bands, trend strength.
* **Sentiment** → Reddit discussion signals.
* **Overall Summary** → Clear takeaway for the investor.

📸 *Example News Report:*

| Date   | Headline                            | Sentiment |
| ------ | ----------------------------------- | --------- |
| Aug 18 | Crypto Inflows Reach \$3.75 Billion | Positive  |
| Aug 14 | US Treasury Won’t Buy Bitcoin       | Negative  |
| Aug 11 | Ethereum Outpaces Bitcoin YTD Gains | Negative  |

**Summary (auto-generated):**

> The recent news paints a mixed picture for Bitcoin. While overall market inflows are positive, Bitcoin is consistently overshadowed by Ethereum’s performance. Short-term outlook leans negative, but long-term adoption remains strong.

---

## ⚙️ Tech Stack

* **Python** (core logic)
* **LangGraph & LangChain** (multi-agent orchestration)
* **Streamlit** (frontend dashboard)
* **CoinGecko API** (fundamentals & price data)
* **CryptoPanic / Google News / Reddit APIs** (news & sentiment)
* **pandas, pandas-ta** (indicators & data processing)

---

## 🏗️ Project Structure

```
├── agents/  
│   ├── news_agent.py          # Fetches crypto news  
│   ├── fundamental_agent.py   # Collects fundamentals  
│   ├── technical_agent.py     # Computes RSI, MACD, Bollinger Bands  
│   ├── sentiment_agent.py     # Reddit sentiment scraper  
│
├── tools.py                   # Shared LangChain tools for agents  
├── app.py                     # Streamlit frontend (main dashboard)  
├── graph.py                   # LangGraph workflow (agent orchestration)  
├── README.md                  # Project documentation  
```

---

## 🛠️ Setup & Run

1️⃣ Clone the repo:

```bash
git clone https://github.com/bhavadharanik/NeutroFi.git
cd NeutroFi
```

2️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

3️⃣ Add API keys (if required) in `.env`:

```
COINGECKO_API_KEY=your_key_here
CRYPTO_PANIC_KEY=your_key_here
```

4️⃣ Run Streamlit app:

```bash
streamlit run app.py
```

---

## 🎯 Example Workflow

1. Run the dashboard.
2. Select **Bitcoin**, mark yourself as **New Buyer**, set **Short Term (1–3 months)**.
3. Click **Run Analytics**.
4. NeutroFi gathers **news, fundamentals, technicals, sentiment**, and produces a **final verdict**:

👉 *“Hold – Confidence 0.70. New entry not advised unless confidence and long-term view are strong.”*

---

## 📌 Future Improvements

* Add more coins & DeFi protocols.
* Enhance sentiment analysis using transformer-based models.
* Introduce portfolio tracking & personalized alerts.
* Multi-language support for international investors.

---

## 👥 Team – Neural Nomads

* **Bhavadharani Kanagaraj**
* **Maneesha Sandagomi**
* **Sivagar Rajasekaran**
* **Samuel Sonowo**

---

🔥 NeutroFi turns **complex crypto data** into **simple, actionable insights** — helping investors cut through noise and make confident decisions.


See it in action : https://neutrofi.streamlit.app/
