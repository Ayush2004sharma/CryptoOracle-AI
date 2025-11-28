from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage
import json


def create_crypto_news_analyst(llm, toolkit):
    def news_analyst_node(state):
        coin = state["coin"]
        current_date = state["trade_date"]

        tools = [toolkit.get_crypto_news]

        # print(f"[🧪] Running news analysis for: {coin}")

        # Properly escaped system message
        system_message = (
            f"You are a cryptocurrency news analyst. You have called the 'get_crypto_news' tool to fetch recent news articles about {coin}. "
            f"The tool output is provided in the messages as a JSON string containing a list of news articles with fields: Title, Published, URL. "
            f"Analyze the news to determine current market sentiment, risks, and opportunities. "
            f"Include a markdown table with columns: Date (Published), Headline (max 50 characters), Sentiment (Positive/Negative/Neutral). "
            f"Provide a professional summary of the major themes and their impact on {coin}'s market perception or price potential. "
            f"If the tool output indicates an error or no news (e.g., {{{{'error': 'message'}}}} or empty list)..."
            f"Example output:\n"
            f"## News Report for {coin}\n"
            f"[Analysis of news items and their impact]\n"
            f"| Date | Headline  | Sentiment |\n|------|----------|--------|-----------|\n| Jan 01 2025 | {coin} hits $100K  | Positive |\n| Jan 02 2025 | Mining concerns  | Negative |\n\n"
            f"**Summary**: [Impact of news on {coin}'s market position].\n"
            f"Do not call the 'get_crypto_news' tool again; use the provided tool output to generate the report."
        )

        # Prompt for first LLM call (tool-calling)
        tool_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a crypto analyst AI.\n"
                    "Immediately call the 'get_crypto_news' tool to fetch recent news for {coin}.\n"
                    "Do not ask for clarification or additional input; use the provided coin symbol.\n"
                    "Date: {current_date}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(current_date=current_date, coin=coin)

        # Prompt for second LLM call (report generation)
        report_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(current_date=current_date, coin=coin)

        # Chains
        tool_chain = tool_prompt | llm
        report_chain = report_prompt | llm

        # STEP 1: Tool execution
        tool_result = tool_chain.invoke(
            {"messages": [{"type": "human", "content": f"Analyze news for {coin}."}]}
        )

        # print(f"[🧪] First result.tool_calls: {tool_result.tool_calls}")

        # Get tool output
        if tool_result.tool_calls:
            tool_call = tool_result.tool_calls[0]
            tool_output = toolkit.get_crypto_news.invoke(
                tool_call["args"]
            )  # Fix deprecated call
            # print(f"[🧪] Tool output: {tool_output}")

            if "error" in tool_output:
                tool_msg = ToolMessage(
                    content=json.dumps(tool_output),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            else:
                tool_msg = ToolMessage(
                    content=json.dumps(tool_output),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
        else:
            tool_msg = ToolMessage(
                content=json.dumps({"error": "No tool call made."}),
                name="get_crypto_news",
                tool_call_id="fallback-id",
            )

        # STEP 2: Run the report
        report = report_chain.invoke({"messages": [tool_result, tool_msg]})
        return {
            "messages": [report],
            "news_report": report.content,
        }

    return news_analyst_node
