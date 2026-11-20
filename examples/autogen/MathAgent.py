# Microsoft Autogen Tool Example
#
# agentlens automatically configures itself when it's initialized meaning your agent run data will be tracked and logged to your agentlens account right away.
# First let's install the required packages
# %pip install -U autogen-agentchat
# %pip install -U "autogen-ext[openai]"
# %pip install -U agentlens
# %pip install -U python-dotenv
# Then import them
from typing import Annotated, Literal
import asyncio
import os
from dotenv import load_dotenv

import agentlens

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

# Next, we'll set our API keys. There are several ways to do this, the code below is just the most foolproof way for the purposes of this notebook. It accounts for both users who use environment variables and those who just want to set the API Key here in this notebook.
#
# [Get an agentlens API key](https://github.com/jeanvaldez10/agent-lens/settings/projects)
#
# 1. Create an environment variable in a .env file or other method. By default, the agentlens `init()` function will look for an environment variable named `AGENTLENS_API_KEY`. Or...
#
# 2. Replace `<your_agentlens_key>` below and pass in the optional `api_key` parameter to the agentlens `init(api_key=...)` function. Remember not to commit your API key to a public repo!
load_dotenv()
os.environ["AGENTLENS_API_KEY"] = os.getenv("AGENTLENS_API_KEY", "your_api_key_here")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

agentlens.init(auto_start_session=False, trace_name="Autogen Math Agent Example")
tracer = agentlens.start_trace(
    trace_name="Microsoft Autogen Tool Example", tags=["autogen-tool", "microsoft-autogen", "agentlens-example"]
)

# AG2 will now start automatically tracking
#
# * LLM prompts and completions
# * Token usage and costs
# * Agent names and actions
# * Correspondence between agents
# * Tool usage
# * Errors
# # Tool Example
# agentlens tracks when AG2 agents use tools. You can find more information on this example in [tool-use.ipynb](https://docs.ag2.ai/docs/tutorial/tool-use#tool-use)
# # Define model and API key
model_name = "gpt-4-turbo"
api_key = os.getenv("OPENAI_API_KEY")

# Create the model client
model_client = OpenAIChatCompletionClient(model=model_name, api_key=api_key, seed=42, temperature=0)

Operator = Literal["+", "-", "*", "/"]


def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


async def main():
    assistant = AssistantAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. You can help with simple calculations. Return 'TERMINATE' when the task is done.",
        model_client=model_client,
        tools=[calculator],
        reflect_on_tool_use=True,
    )

    initial_task_message = "What is (1423 - 123) / 3 + (32 + 23) * 5?"
    print(f"User Task: {initial_task_message}")

    try:
        from autogen_core import CancellationToken

        response = await assistant.on_messages(
            [TextMessage(content=initial_task_message, source="user")], CancellationToken()
        )

        final_response_message = response.chat_message
        if final_response_message:
            print(f"Assistant: {final_response_message.to_text()}")
        else:
            print("Assistant did not provide a final message.")

        agentlens.end_trace(tracer, end_state="Success")

    except Exception as e:
        print(f"An error occurred: {e}")
        agentlens.end_trace(tracer, end_state="Error")
    finally:
        await model_client.close()

    # Let's check programmatically that spans were recorded in agentlens
    print("\n" + "=" * 50)
    print("Now let's verify that our LLM calls were tracked properly...")
    try:
        agentlens.validate_trace_spans(trace_context=tracer)
        print("\n✅ Success! All LLM spans were properly recorded in agentlens.")
    except agentlens.ValidationError as e:
        print(f"\n❌ Error validating spans: {e}")
        raise


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio

        nest_asyncio.apply()
        asyncio.run(main())
    else:
        asyncio.run(main())

# You can see your run in action at [app.github.com/jeansvaldez/agentlens](app.github.com/jeansvaldez/agentlens). In this example, the agentlens dashboard will show:
#
# * Agents talking to each other
# * Each use of the `calculator` tool
# * Each call to OpenAI for LLM use
