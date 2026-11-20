"""agentlens semantic conventions for spans."""

from agentlens.semconv.span_kinds import SpanKind
from agentlens.semconv.core import CoreAttributes
from agentlens.semconv.agent import AgentAttributes
from agentlens.semconv.tool import ToolAttributes
from agentlens.semconv.status import ToolStatus
from agentlens.semconv.workflow import WorkflowAttributes
from agentlens.semconv.instrumentation import InstrumentationAttributes
from agentlens.semconv.enum import LLMRequestTypeValues
from agentlens.semconv.span_attributes import SpanAttributes
from agentlens.semconv.meters import Meters
from agentlens.semconv.span_kinds import agentlensSpanKindValues
from agentlens.semconv.resource import ResourceAttributes
from agentlens.semconv.message import MessageAttributes
from agentlens.semconv.langchain import LangChainAttributes, LangChainAttributeValues

SUPPRESS_LANGUAGE_MODEL_INSTRUMENTATION_KEY = "suppress_language_model_instrumentation"
__all__ = [
    "SUPPRESS_LANGUAGE_MODEL_INSTRUMENTATION_KEY",
    "SpanKind",
    "CoreAttributes",
    "AgentAttributes",
    "ToolAttributes",
    "ToolStatus",
    "WorkflowAttributes",
    "InstrumentationAttributes",
    "LLMRequestTypeValues",
    "SpanAttributes",
    "Meters",
    "agentlensSpanKindValues",
    "ResourceAttributes",
    "MessageAttributes",
    "LangChainAttributes",
    "LangChainAttributeValues",
]
