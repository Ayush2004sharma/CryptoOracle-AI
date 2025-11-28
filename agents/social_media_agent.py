# agents/social_media_agent.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage


def create_sentiment_analyst(llm, toolkit):
    def sentiment_analyst_node(state):
        coin = state["coin"]
        current_date = state["trade_date"]

        # Uses the existing tool from the toolkit
        tools = [toolkit.get_reddit_sentiment_posts]

        system_message = (
            f"You are a social media sentiment analyst. You have called the "
            f"'get_reddit_sentiment_posts' tool to fetch recent social and news posts "
            f"related to {coin}. These posts come from sources like Twitter/X and "
            f"CryptoPanic news.\n\n"
            f"The tool output is provided in the messages. Classify each post as "
            f"Positive (e.g., optimistic, bullish), Negative (e.g., critical, bearish), "
            f"or Neutral (e.g., factual, no strong opinion).\n"
            f"Provide a markdown table with columns: Post (short excerpt, max 50 characters), "
            f"Sentiment, Reason.\n"
            f"Summarize the overall market mood (e.g., Bullish, Bearish, Neutral).\n\n"
            f"If the tool output is 'No recent posts found for this coin.' or similar, "
            f"return a report stating:\n"
            f"| Post | Sentiment | Reason |\n"
            f"|------|-----------|--------|\n"
            f"| No posts found | Neutral | No recent posts available |\n\n"
            f"**Summary**: No recent posts found for {coin}. Consider checking other "
            f"sources like market news, on-chain data, or longer-term fundamentals.\n\n"
            f"Example output:\n"
            f"| Post | Sentiment | Reason |\n"
            f"|------|-----------|--------|\n"
            f"| Bitcoin to the moon! | Positive | Optimistic about price |\n"
            f"| BTC is crashing | Negative | Bearish sentiment |\n\n"
            f"**Summary**: Mixed sentiment with cautious outlook.\n\n"
            f"Do not call the 'get_reddit_sentiment_posts' tool again; "
            f"use the provided tool output to generate the report."
        )

        # Prompt for first LLM call (with tool-calling)
        tool_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI sentiment analyst.\n"
                    "You have access to the following tools: {tool_names}.\n"
                    "Use the 'get_reddit_sentiment_posts' tool to fetch recent social/news "
                    "posts for {coin}.\n"
                    "Date: {current_date}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(
            current_date=current_date,
            tool_names=", ".join([tool.name for tool in tools]),
            coin=coin,
        )

        # Prompt for second LLM call (without tool-calling)
        report_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(current_date=current_date, coin=coin)

        # Chain for first call (with tools)
        tool_chain = tool_prompt | llm

        # Chain for second call (no tools to prevent re-triggering)
        report_chain = report_prompt | llm

        # STEP 1: First LLM call triggers tool
        result = tool_chain.invoke(state["messages"])

        # STEP 2: If tools were triggered, call them and re-run LLM
        if result.tool_calls:
            tool_outputs = []
            for tool_call in result.tool_calls:
                tool_name = tool_call["name"]
                args = tool_call["args"]
                tool_func = getattr(toolkit, tool_name)
                tool_output = tool_func.invoke(args)

                # Ensure tool_output is not empty
                if not tool_output or tool_output.strip() == "":
                    tool_output = "No recent posts found for this coin."

                # Wrap tool output as ToolMessage
                tool_outputs.append(
                    ToolMessage(
                        content=tool_output,
                        tool_call_id=tool_call["id"],
                        name=tool_name,
                    )
                )

            state["messages"].append(result)        # AIMessage with tool calls
            state["messages"].append(tool_outputs[0])  # ToolMessage

            # STEP 3: Re-run LLM with report prompt (no tools)
            try:
                result = report_chain.invoke(state["messages"])
            except Exception as e:
                return {
                    "messages": state["messages"],
                    "sentiment_report": f"Error: Failed to generate report due to {str(e)}",
                }

            # Check for unexpected tool calls
            if result.tool_calls:
                simplified_messages = [
                    state["messages"][0],  # Original HumanMessage
                    tool_outputs[0],       # ToolMessage
                ]
                try:
                    result = report_chain.invoke(simplified_messages)
                except Exception as e:
                    return {
                        "messages": state["messages"],
                        "sentiment_report": f"Error: Failed to generate report on retry due to {str(e)}",
                    }

        report = result.content or "⚠️ No report generated."

        return {
            "messages": [result],
            "sentiment_report": report,
        }

    return sentiment_analyst_node
