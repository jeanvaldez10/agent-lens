from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture(scope="function")
def llm_event_spy(agentlens_client, mocker: "MockerFixture") -> dict[str, "MockerFixture"]:
    """
    Fixture that provides spies on both providers' response handling

    These fixtures are reset on each test run (function scope). To use it,
    simply pass it as an argument to the test function. Example:

    ```
    def test_my_test(llm_event_spy):
        # test code here
        llm_event_spy["litellm"].assert_called_once()
    ```
    """
    from agentlens.llms.providers.anthropic import AnthropicProvider
    from agentlens.llms.providers.litellm import LiteLLMProvider
    from agentlens.llms.providers.openai import OpenAiProvider

    return {
        "litellm": mocker.spy(LiteLLMProvider(agentlens_client), "handle_response"),
        "openai": mocker.spy(OpenAiProvider(agentlens_client), "handle_response"),
        "anthropic": mocker.spy(AnthropicProvider(agentlens_client), "handle_response"),
    }
