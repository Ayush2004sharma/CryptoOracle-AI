from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage
import json


def create_fundamentals_analyst(llm, toolkit):
    def fundamentals_analyst_node(state):
        coin = state["coin"]
        current_date = state["trade_date"]

        tools = [toolkit.get_crypto_fundamentals]

        STRICT_SYSTEM = f"""
You are a STRICT crypto fundamentals analyst.

RULES YOU MUST FOLLOW:

1. You MUST use ONLY the data provided in the tool output.
2. If ANY information is missing, write: "Not Available".
3. DO NOT guess, assume, or generate invented numbers or facts.
4. DO NOT infer values from market averages or past trends.
5. DO NOT add external information (GitHub commits, mining stats, regulatory status, etc.) unless directly present in the tool output.
6. DO NOT include projections, opinions, predictions, or speculation.

OUTPUT FORMAT:

## Fundamentals Report for {coin}

| Metric | Value |
|--------|------|
| Current Price | value |
| Market Cap | value |
| 24H Volume | value |
| Circulating Supply | value |
| Total Supply | value |
| Max Supply | value |
| Market Rank | value |

**Summary**
Write 2–4 sentences strictly describing the data. 
If values are missing, state: "Data incomplete — unable to form full analysis."

If the tool output indicates an error or is empty, say:

⚠️ No fundamental data available for {coin}.
"""

        # Prompt for tool request
        tool_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Call the 'get_crypto_fundamentals' tool immediately to retrieve factual data for {coin}. "
                    "Do not ask questions. Do not reason. Just call the tool."
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(coin=coin)

        # Prompt for final formatted report
        report_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STRICT_SYSTEM),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(coin=coin, current_date=current_date)

        tool_chain = tool_prompt | llm
        report_chain = report_prompt | llm

        # Step 1 — Trigger tool call
        result = tool_chain.invoke(state["messages"])

        # Step 2 — Execute tool if called
        if result.tool_calls:
            tool_call = result.tool_calls[0]
            tool_func = getattr(toolkit, tool_call["name"])
            tool_output = tool_func.invoke(tool_call["args"])

            # Empty output handling
            if not tool_output or tool_output.strip() == "":
                tool_output = json.dumps({"error": f"No data available for {coin}"})

            # Wrap in ToolMessage
            tool_message = ToolMessage(
                content=tool_output,
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )

            state["messages"].append(result)
            state["messages"].append(tool_message)

            # Step 3 — Second pass (Generate report)
            result = report_chain.invoke({"messages": state["messages"]})

        final_report = result.content or f"⚠️ No fundamental data available for {coin}."

        return {
            "messages": [result],
            "fundamentals_report": final_report,
        }

    return fundamentals_analyst_node
