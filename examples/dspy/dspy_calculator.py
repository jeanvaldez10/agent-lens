import os

import dspy
from dspy import Tool
import agentlens
from agentlens.integration.callbacks.dspy import DSPyCallbackHandler

from dotenv import load_dotenv

load_dotenv()

handler = DSPyCallbackHandler(api_key=os.getenv("AGENTLENS_API_KEY", ""), cache=False)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

lm = dspy.LM("openai/gpt-4o-mini", temperature=0.5)
dspy.configure(lm=lm, callbacks=[handler])


def multiplier(*, a: int, b: int) -> int:
    return a * b


multiplier = Tool(multiplier)

agent = dspy.ProgramOfThought("question -> answer: int")
response = agent(question="What is twenty five times twenty five?", tools=[multiplier])

print(response)
print("Now let's verify that our LLM calls were tracked properly...")

try:
    agentlens.validate_trace_spans(trace_context=None)
    print("\n✅ Success! All LLM spans were properly recorded in agentlens.")
except ImportError:
    print("\n❌ Error: agentlens library not installed. Please install it to validate spans.")
except agentlens.ValidationError as e:
    print(f"\n❌ Error validating spans: {e}")
    raise
