# # OpenAI Agents Guardrails Demonstration
#
# This notebook demonstrates guardrails using the Agents SDK and how one can observe them using the agentlens platform.

# Install required packages
# %pip install agentlens
# %pip install openai-agents
# %pip install dotenv pydantic

# Import dependencies
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

# Initialize agentlens and import the guardrail decorator
import agentlens
from agentlens import guardrail

# Load API keys
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

os.environ["AGENTLENS_API_KEY"] = os.getenv("AGENTLENS_API_KEY", "your_api_key_here")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

agentlens.init(api_key=os.environ["AGENTLENS_API_KEY"], trace_name="OpenAI Agents Guardrails", tags=["agentlens-example"])


# OpenAI Agents SDK guardrail example with agentlens guardrails decorator for observability
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
@guardrail(spec="input")  # Specify guardrail type as input or output
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)


async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")


if __name__ == "__main__":
    asyncio.run(main())


# Let's check programmatically that spans were recorded in agentlens
print("\n" + "=" * 50)
print("Now let's verify that our LLM calls were tracked properly...")
try:
    agentlens.validate_trace_spans(trace_context=None)
    print("\n✅ Success! All LLM spans were properly recorded in agentlens.")
except agentlens.ValidationError as e:
    print(f"\n❌ Error validating spans: {e}")
    raise
