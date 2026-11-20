# OpenAI Sync Example
#
# We are going to create a simple chatbot that creates stories based on a prompt. The chatbot will use the gpt-4o-mini LLM to generate the story using a user prompt.
#
# We will track the chatbot with agentlens and see how it performs!
# First let's install the required packages
# # Install required dependencies
# %pip install agentlens
# %pip install openai
# %pip install python-dotenv
# Then import them
from openai import OpenAI
import agentlens
import os
from dotenv import load_dotenv

# Next, we'll grab our API keys. You can use dotenv like below or however else you like to load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
os.environ["AGENTLENS_API_KEY"] = os.getenv("AGENTLENS_API_KEY", "your_api_key_here")

# Next we initialize the agentlens client.
agentlens.init(auto_start_session=True, trace_name="OpenAI Sync Example", tags=["openai", "sync", "agentlens-example"])
tracer = agentlens.start_trace(
    trace_name="OpenAI Sync Example", tags=["openai-sync-example", "openai", "agentlens-example"]
)
client = OpenAI()

# And we are all set! Note the seesion url above. We will use it to track the chatbot.
#
# Let's create a simple chatbot that generates stories.
system_prompt = """
You are a master storyteller, with the ability to create vivid and engaging stories.
You have experience in writing for children and adults alike.
You are given a prompt and you need to generate a story based on the prompt.
"""

user_prompt = "Write a very short story about a cyber-warrior trapped in the imperial time period."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(response.choices[0].message.content)

# The response is a string that contains the story. We can track this with agentlens by navigating to the trace url and viewing the run.
# ## Streaming Version
# We will demonstrate the streaming version of the API.
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True,
)

for chunk in stream:
    if chunk.choices and len(chunk.choices) > 0:
        print(chunk.choices[0].delta.content or "", end="")

agentlens.end_trace(tracer, end_state="Success")

# Let's check programmatically that spans were recorded in agentlens
print("\n" + "=" * 50)
print("Now let's verify that our LLM calls were tracked properly...")
try:
    result = agentlens.validate_trace_spans(trace_context=tracer)
    agentlens.print_validation_summary(result)
except agentlens.ValidationError as e:
    print(f"\n❌ Error validating spans: {e}")
    raise

# Note that the response is a generator that yields chunks of the story. We can track this with agentlens by navigating to the trace url and viewing the run.
# All done!
