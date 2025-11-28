# risk_management_agent.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage


def create_risk_manager_agent(llm):
    def risk_manager_node(state):
        coin = state["coin"]
        current_date = state["trade_date"]

        user_type = state.get("user_type", "holder")  # 'holder' or 'buyer'
        horizon = state.get("horizon", "long")  # 'short', 'medium', 'long'

        decision = state.get("research_decision", "Hold").capitalize()
        confidence = state.get("research_confidence", 0.5)
        research_summary = state.get(
            "research_summary", "No research summary available."
        )

        # Time horizon forecasts fallback
        horizon_forecasts = state.get(
            "horizon_forecasts",
            {
                "short_term": {"recommendation": decision, "confidence": confidence},
                "medium_term": {"recommendation": decision, "confidence": confidence},
                "long_term": {"recommendation": decision, "confidence": confidence},
            },
        )

        def norm(val):
            return val.capitalize() if isinstance(val, str) else val

        short_term_rec = norm(
            horizon_forecasts["short_term"].get("recommendation", decision)
        )
        short_term_conf = horizon_forecasts["short_term"].get("confidence", confidence)

        medium_term_rec = norm(
            horizon_forecasts["medium_term"].get("recommendation", decision)
        )
        medium_term_conf = horizon_forecasts["medium_term"].get(
            "confidence", confidence
        )

        long_term_rec = norm(
            horizon_forecasts["long_term"].get("recommendation", decision)
        )
        long_term_conf = horizon_forecasts["long_term"].get("confidence", confidence)

        # --- Risk Adjustment Rules ---
        risk_notes = []

        holder_action = decision
        holder_reason = ""
        if confidence < 0.55:
            holder_action = "Hold"
            holder_reason = "Confidence too low for action — defaulting to Hold."
            risk_notes.append(
                "Overall confidence < 0.55 — Holder action downgraded to Hold."
            )
        elif decision == "Buy" and confidence <= 0.7:
            holder_action = "Hold"
            holder_reason = (
                "Buy signal lacks strong confidence — set to Hold for caution."
            )
            risk_notes.append("Buy confidence ≤ 0.7 — Holder action adjusted to Hold.")
        elif decision == "Buy":
            holder_action = "Buy"
            holder_reason = "Strong enough research to proceed with Buy."
            risk_notes.append("Buy confirmed for holder based on overall research.")
        elif decision == "Sell":
            holder_action = "Sell"
            holder_reason = "Sell maintained to prevent downside."
            risk_notes.append("Sell preserved for downside protection.")
        else:
            holder_action = "Hold"
            holder_reason = "No major risk signals — maintaining Hold."

        buyer_action = "Hold"
        buyer_reason = (
            "New entry not advised unless confidence and long-term view are strong."
        )
        if decision == "Buy" and confidence > 0.8 and long_term_conf > 0.75:
            buyer_action = "Buy"
            buyer_reason = (
                "High long-term confidence and overall conviction support new entry."
            )
            risk_notes.append("Strong long-term outlook — Buy allowed for new buyers.")
        else:
            risk_notes.append(
                "New buyers advised to Hold unless long-term confidence is strong."
            )

        # --- Choose final recommendation based on user_type ---
        if user_type == "holder":
            final_action = holder_action
            final_reason = holder_reason
        else:
            final_action = buyer_action
            final_reason = buyer_reason

        # --- Filter horizon-specific recommendation ---
        horizon_map = {
            "short": (short_term_rec, short_term_conf),
            "medium": (medium_term_rec, medium_term_conf),
            "long": (long_term_rec, long_term_conf),
        }
        horizon_rec, horizon_conf = horizon_map.get(
            horizon, (long_term_rec, long_term_conf)
        )

        # --- Prompt for explanation ---
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are a risk management analyst. The trade date is {current_date}.",
                ),
                (
                    "user",
                    """
Based on the research summary, give a FINAL risk-adjusted recommendation 
only for the specified trader type and investment horizon.

Trader Type: {user_type}
Investment Horizon: {horizon}
Recommendation: {final_action}
Reason: {final_reason}

Horizon Forecast:
{horizon} term: {horizon_rec} ({horizon_conf})

Risk Notes:
{risk_notes}

Research Summary:
{summary}
                    """,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(
            user_type=user_type,
            horizon=horizon,
            final_action=final_action,
            final_reason=final_reason,
            horizon_rec=horizon_rec,
            horizon_conf=horizon_conf,
            risk_notes="\n".join(risk_notes),
            summary=research_summary,
        )

        chain = prompt | llm

        try:
            result = chain.invoke({"messages": state.get("messages", [])})
            return {
                "messages": [AIMessage(content=result.content)],
                "final_recommendation": final_action,
                "final_reason": final_reason,
                "confidence": horizon_conf,
                "risk_notes": "\n".join(risk_notes),
            }
        except Exception as e:
            return {
                "messages": state.get("messages", []),
                "final_recommendation": "Hold",
                "final_reason": f"Error during decision evaluation: {e}",
                "confidence": 0.5,
                "risk_notes": f"Error during risk check: {e}",
            }

    return risk_manager_node
