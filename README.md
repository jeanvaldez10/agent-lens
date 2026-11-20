<div align="center">
  <h1>Agentlens</h1>
</div>

<div align="center">
  <em>Observability and DevTool platform for AI Agents</em>
</div>

<br />

<br/>

agentlens helps developers build, evaluate, and monitor AI agents. From prototype to production.

## Open Source

The agentlens app is open source under the MIT license. Explore the code in our [app directory](https://github.com/jeansvaldez/agentlens/tree/main/app).

## Key Integrations 🔌


| 📊 **Replay Analytics and Debugging** | Step-by-step agent execution graphs                           |
| 💸 **LLM Cost Management**            | Track spend with LLM foundation model providers               |
| 🤝 **Framework Integrations**         | Native Integrations with CrewAI, AG2 (AutoGen), Agno, LangGraph, & more         |
| ⚒️ **Self-Host**                      | Want to run agentlens on your own cloud? You're covered        |

## Quick Start ⌨️

```bash
pip install agentlens
```


#### Session replays in 2 lines of code

Initialize the agentlens client and automatically get analytics on all your LLM calls.

[Get an API key](http://localhost:3000/settings/projects)

```python
import agentlens

# Beginning of your program (i.e. main.py, __init__.py)
agentlens.init( < INSERT YOUR API KEY HERE >)

...

# End of program
agentlens.end_session('Success')
```

All your sessions can be viewed on the [agentlens dashboard](http://localhost:3000?ref=gh)
<br/>

## Self-Hosting

Looking to run the full agentlens app (Dashboard + API backend) on your machine? Follow the setup guide in `app/README.md`:

- [Run the App and Backend (Dashboard + API)](app/README.md)



### First class Developer Experience
Add powerful observability to your agents, tools, and functions with as little code as possible: one line at a time.
<br/>
Refer to our [documentation](https://github.com/jeansvaldez/agentlens)

```python
# Create a session span (root for all other spans)
from agentlens.sdk.decorators import session

@session
def my_workflow():
    # Your session code here
    return result
```

```python
# Create an agent span for tracking agent operations
from agentlens.sdk.decorators import agent

@agent
class MyAgent:
    def __init__(self, name):
        self.name = name
        
    # Agent methods here
```

```python
# Create operation/task spans for tracking specific operations
from agentlens.sdk.decorators import operation, task

@operation  # or @task
def process_data(data):
    # Process the data
    return result
```

```python
# Create workflow spans for tracking multi-operation workflows
from agentlens.sdk.decorators import workflow

@workflow
def my_workflow(data):
    # Workflow implementation
    return result
```

```python
# Nest decorators for proper span hierarchy
from agentlens.sdk.decorators import session, agent, operation

@agent
class MyAgent:
    @operation
    def nested_operation(self, message):
        return f"Processed: {message}"
        
    @operation
    def main_operation(self):
        result = self.nested_operation("test message")
        return result

@session
def my_session():
    agent = MyAgent()
    return agent.main_operation()
```

All decorators support:
- Input/Output Recording
- Exception Handling
- Async/await functions
- Generator functions
- Custom attributes and names


## Evaluations Roadmap 🧭

| Platform                                                                     | Dashboard                                  | Evals                                  |
| ---------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------- |
| ✅ Python SDK                                                                | ✅ Multi-session and Cross-session metrics | ✅ Custom eval metrics                 |
| 🚧 Evaluation builder API                                                    | ✅ Custom event tag tracking              | 🔜 Agent scorecards                    |
| 🚧 [Javascript/Typescript SDK (Alpha)](https://github.com/jeansvaldez/agentlens-node) | ✅ Session replays                         | 🔜 Evaluation playground + leaderboard |

## Debugging Roadmap 🧭

| Performance testing                       | Environments                                                                        | LLM Testing                                 | Reasoning and execution testing                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------- |
| ✅ Event latency analysis                 | 🔜 Non-stationary environment testing                                               | 🔜 LLM non-deterministic function detection | 🚧 Infinite loops and recursive thought detection |
| ✅ Agent workflow execution pricing       | 🔜 Multi-modal environments                                                         | 🚧 Token limit overflow flags               | 🔜 Faulty reasoning detection                     |
| 🚧 Success validators (external)          | 🔜 Execution containers                                                             | 🔜 Context limit overflow flags             | 🔜 Generative code validators                     |
| 🔜 Agent controllers/skill tests          | ✅ Honeypot and prompt injection detection ([PromptArmor](https://promptarmor.com)) | ✅ API bill tracking                        | 🔜 Error breakpoint analysis                      |
| 🔜 Information context constraint testing | 🔜 Anti-agent roadblocks (i.e. Captchas)                                            | 🔜 CI/CD integration checks                 |                                                   |
| 🔜 Regression testing                     | ✅ Multi-agent framework visualization                                              |                                             |                                                   |

### Why Agentlens? 🤔

Without the right tools, AI agents are slow, expensive, and unreliable. Our mission is to bring your agent from prototype to production. Here's why agentlens stands out:

- **Comprehensive Observability**: Track your AI agents' performance, user interactions, and API usage.
- **Real-Time Monitoring**: Get instant insights with session replays, metrics, and live monitoring tools.
- **Cost Control**: Monitor and manage your spend on LLM and API calls.
- **Failure Detection**: Quickly identify and respond to agent failures and multi-agent interaction issues.
- **Tool Usage Statistics**: Understand how your agents utilize external tools with detailed analytics.
- **Session-Wide Metrics**: Gain a holistic view of your agents' sessions with comprehensive statistics.
Agentlens is designed to make agent observability, testing, and monitoring easy.


## Star History

Check out our growth in the community:


## Popular projects using agentlens


| Repository | Stars  |
| :--------  | -----: |


_Generated using [github-dependents-info](https://github.com/nvuillam/github-dependents-info), by [Nicolas Vuillamy](https://github.com/nvuillam)_
