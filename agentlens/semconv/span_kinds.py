"""Span kinds for agentlens."""

from enum import Enum


class agentlensSpanKindValues(Enum):
    """Standard span kind values for agentlens."""

    WORKFLOW = "workflow"
    SESSION = "session"
    TASK = "task"
    OPERATION = "operation"
    AGENT = "agent"
    TOOL = "tool"
    LLM = "llm"
    CHAIN = "chain"
    TEXT = "text"
    GUARDRAIL = "guardrail"
    HTTP = "http"
    UNKNOWN = "unknown"


# Legacy SpanKind class for backward compatibility
class SpanKind:
    """Legacy span kind definitions - use agentlensSpanKindValues instead."""

    # Agent action kinds
    AGENT_ACTION = "agent.action"  # Agent performing an action
    AGENT_THINKING = "agent.thinking"  # Agent reasoning/planning
    AGENT_DECISION = "agent.decision"  # Agent making a decision

    # LLM interaction kinds
    LLM_CALL = "llm.call"  # LLM API call

    # Workflow kinds
    WORKFLOW_STEP = "workflow.step"  # Step in a workflow
    WORKFLOW = agentlensSpanKindValues.WORKFLOW.value
    SESSION = agentlensSpanKindValues.SESSION.value
    TASK = agentlensSpanKindValues.TASK.value
    OPERATION = agentlensSpanKindValues.OPERATION.value
    AGENT = agentlensSpanKindValues.AGENT.value
    TOOL = agentlensSpanKindValues.TOOL.value
    LLM = agentlensSpanKindValues.LLM.value
    UNKNOWN = agentlensSpanKindValues.UNKNOWN.value
    CHAIN = agentlensSpanKindValues.CHAIN.value
    TEXT = agentlensSpanKindValues.TEXT.value
    GUARDRAIL = agentlensSpanKindValues.GUARDRAIL.value
    HTTP = agentlensSpanKindValues.HTTP.value
