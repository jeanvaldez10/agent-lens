import agentlens
from openai import OpenAI
from dotenv import load_dotenv
from agentlens import ActionEvent

load_dotenv()
agentlens.init(default_tags=["canary"])
openai = OpenAI()

messages = [{"role": "user", "content": "Hello"}]

# option 1: use session.patch
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.5,
)

agentlens.record(ActionEvent(action_type="test event"))

agentlens.end_session(end_state="Success")

###
#  Used to verify that one session is created with one LLM event
###
