from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage, AIMessage
import json
import uuid


def create_technical_analyst(llm, toolkit):
    def technical_analyst_node(state):
        coin = state["coin"]
        current_date = state["trade_date"]

        tools = [toolkit.get_crypto_technicals]

        # print(f"[🧪] Running technical analysis for: {coin}")

        # System message for report generation
        system_message = (
            f"You are a cryptocurrency technical analyst. You have called the 'get_crypto_technicals' tool to fetch technical indicators (RSI, MACD, Bollinger Bands) for {coin}. "
            f"The tool output is provided in the messages as a JSON string containing indicators like rsi, macd, macd_signal, bb_lower, bb_upper, bb_middle, close. "
            f"Write a detailed expert-level analysis explaining the technical outlook, highlighting overbought/oversold conditions, momentum, and volatility. "
            f"Include a markdown table with columns: Indicator, Value, Interpretation (e.g., Overbought, Bullish, Neutral). "
            f"Provide a professional summary of the technical outlook (e.g., bullish, bearish, neutral). "
            f"If the tool output is empty or reports an error, state: 'No technical data available for {coin}.'"
            f"Example output:\n"
            f"## Technical Report for {coin}\n"
            f"[Analysis of RSI, MACD, Bollinger Bands...]"
        )

        # Prompt for first LLM call (tool-calling)
        tool_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a crypto analyst AI.\n"
                    "Immediately call the 'get_crypto_technicals' tool to fetch technical indicators for the coin '{coin}'.\n"
                    "Do not ask for clarification or additional input; use the provided coin symbol.\n"
                    "Date: {current_date}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(current_date=current_date, coin=coin)

        # Prompt for second LLM call (report generation, no tools)
        report_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_message,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(current_date=current_date, coin=coin)

        # Chains
        tool_chain = tool_prompt | llm
        report_chain = report_prompt | llm

        # STEP 1: First LLM call to trigger tool
        result = tool_chain.invoke(state["messages"])
        # print(f"[🧪] First result.tool_calls: {result.tool_calls}")
        # print(f"[🧪] First result.content: {result.content}")

        # STEP 2: If no tool call, manually trigger get_crypto_technicals
        if not result.tool_calls:
            # print(
            #     f"[🧪] Warning: No tool calls generated, manually triggering get_crypto_technicals for {coin}"
            # )
            tool_call_id = str(uuid.uuid4())
            result = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "get_crypto_technicals",
                        "args": {"coin": coin},
                        "id": tool_call_id,
                        "type": "tool_call",
                    }
                ],
            )

        # STEP 3: Execute tool calls
        tool_outputs = []
        for tool_call in result.tool_calls:
            tool_name = tool_call["name"]
            args = tool_call["args"]
            # print(f"[🧪] Calling tool: {tool_name} with args: {args}")
            tool_func = getattr(toolkit, tool_name)
            tool_output = tool_func.invoke(args)
            # print(f"[🧪] Tool output: {tool_output}")
            # Ensure tool_output is valid
            if not tool_output or tool_output.strip() == "":
                tool_output = json.dumps(
                    {"error": f"No technical data available for {coin}"}
                )
            # Wrap tool output as ToolMessage
            tool_outputs.append(
                ToolMessage(
                    content=tool_output, tool_call_id=tool_call["id"], name=tool_name
                )
            )

        state["messages"].append(result)  # Append tool_call (AIMessage)
        if tool_outputs:
            state["messages"].append(tool_outputs[0])  # Append ToolMessage

        # Log messages before second invoke
        # print(f"[🧪] Messages before second invoke: {state['messages']}")

        # STEP 4: Re-run LLM with report prompt (no tools)
        try:
            input_dict = {"messages": state["messages"]}
            # print(f"[🧪] Input to report_chain: {input_dict}")
            result = report_chain.invoke(input_dict)
            # print(f"[🧪] Second LLM result: {result}")
        except Exception as e:
            # print(f"[🧪] Error invoking LLM: {e}")
            return {
                "messages": state["messages"],
                "technical_report": f"Error: Failed to generate report due to {str(e)}",
            }

        # Check for unexpected tool calls
        if result.tool_calls:
            # print(
            #     f"[🧪] Warning: Unexpected tool calls in second LLM call: {result.tool_calls}"
            # )
            # Fallback: Retry with simplified messages
            simplified_messages = [
                state["messages"][0],  # Original HumanMessage
                tool_outputs[0],  # ToolMessage
            ]
            try:
                input_dict = {"messages": simplified_messages}
                # print(f"[🧪] Retry input to report_chain: {input_dict}")
                result = report_chain.invoke(input_dict)
                # print(f"[🧪] Retry LLM result: {result}")
            except Exception as e:
                # print(f"[🧪] Retry failed: {e}")
                return {
                    "messages": state["messages"],
                    "technical_report": f"Error: Failed to generate report on retry due to {str(e)}",
                }

        report = result.content or f"No technical data available for {coin}."
        # print(f"[🧪] Final report: {report}")

        return {
            "messages": [result],
            "technical_report": report,
        }

    return technical_analyst_node
