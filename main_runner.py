from graph import graph  # make sure this imports your compiled LangGraph
from datetime import datetime
import re


def run_trading_pipeline(
    coin: str,
    trade_date: str = None,
    trader_position: str = "existing_buyer",
    duration: str = "short_term",
):
    if trade_date is None:
        trade_date = datetime.today().strftime("%Y-%m-%d")

    state = {
        "coin": coin,
        "trade_date": trade_date,
        "user_type": trader_position,
        "horizon": duration,
        "messages": [],
        "news_report": None,
        "fundamentals_report": None,
        "technical_report": None,
        "sentiment_report": None,
        "research_summary": None,
        "risk_notes": None,
        "final_recommendation": None,
        "research_decision": None,
        "research_confidence": None,
        "final_reason": None,
        "confidence": None,
    }

    print(
        f"\n🚀 Starting pipeline for: {coin} ({trader_position}, {duration}) on {trade_date}\n"
    )
    final_state = graph.invoke(state)

    # === Build structured output ===
    structured_output = {
        "coin": coin,
        "trade_date": trade_date,
        "final_decision": final_state.get("final_recommendation", ""),
        "research_summary": final_state.get("research_summary", ""),
        "risk_notes": final_state.get("risk_notes", ""),

        "trader_position": final_state.get("user_type", trader_position),
        "horizon": final_state.get("horizon", duration),
        "confidence":  final_state.get("confidence"),
        "final_reason": final_state.get("final_reason"),

        "reports": {
            "news": {"raw": final_state.get("news_report", "")},
            "fundamentals": {"raw": final_state.get("fundamentals_report", "")},
            "technical": {"raw": final_state.get("technical_report", "")},
            "sentiment": {"raw": final_state.get("sentiment_report", "")},
            "overall": {"raw": final_state.get("research_summary", "")},
        },
    }

    # === Keep old prints for CLI debugging ===
    print("\n✅ Final Decision Output\n")
    print("📰 News Report:\n", final_state.get("news_report", "N/A"))
    print("\n📊 Fundamentals Report:\n", final_state.get("fundamentals_report", "N/A"))
    print("\n📉 Technical Report:\n", final_state.get("technical_report", "N/A"))
    print("\n💬 Sentiment Report:\n", final_state.get("sentiment_report", "N/A"))
    print("\n🔬 Research Summary:\n", final_state.get("research_summary", "N/A"))
    # print("\n⚠️ Risk Notes:\n", final_state.get("risk_notes", "N/A"))
    print("\n📈 Final Decision:\n", final_state.get("final_recommendation", "N/A"))
    print("\n Horizon Forecast:\n", final_state.get("horizon", "N/A"))
    print("\n Confidence Score:\n", final_state.get("confidence", "N/A"))
    print("\n Reasons for Decision:\n", final_state.get("final_reason", "N/A"))
    print("\n✅ Pipeline complete.")

    return structured_output


if __name__ == "__main__":
    # Modify this line to run for different coins or dates
    run_trading_pipeline(
        coin="eth",
        trade_date="2025-08-05",
        trader_position="new_buyer",
        duration="short_term",
    )
