from enum import Enum
from typing import Any, Dict

from opentelemetry.semconv._incubating.attributes.gen_ai_attributes import (
    GEN_AI_OPERATION_NAME,
    GEN_AI_REQUEST_MODEL,
    GEN_AI_RESPONSE_MODEL,
    GEN_AI_SYSTEM,
    GenAiOperationNameValues,
)
from opentelemetry.semconv_ai import LLMRequestTypeValues, SpanAttributes
from opentelemetry.trace import SpanKind

from agentlens.api.encoders.spans import SpanAttributeEncoder


# ==========================================
# Internal Span Classifications
# ==========================================
class AgentlensSpanType(str, Enum):
    """Internal classification of span types for agentlens processing."""

    SESSION_UPDATE = "session_update"
    GEN_AI = "gen_ai"
    LOG = "log"


class AgentlensGenAISpanSubtype(str, Enum):
    """Internal classification of GenAI span subtypes for agentlens processing.

    Note: These are NOT OpenTelemetry standard span types, but rather
    internal classifications used by agentlens for processing."""

    CHAT = "gen_ai_chat"
    COMPLETION = "gen_ai_completion"
    TOOL = "gen_ai_tool"
    EMBEDDING = "gen_ai_embedding"
    GENERIC = "gen_ai"  # Generic/fallback type


# Legacy/alternative attributes (used in some implementations)
LEGACY_SYSTEM = "ai.system"
LEGACY_LLM = "ai.llm"
LEGACY_EMBEDDING = "ai.embedding"

# Tool attributes - these aren't yet in the standard, so we define them here
GEN_AI_TOOL_NAME = "gen_ai.tool.name"
GEN_AI_TOOL_CALL_ID = "gen_ai.tool.call.id"

# Log attributes
LOG_SEVERITY = "log.severity"
LOG_MESSAGE = "log.message"


async def classify_span(span: Dict[str, Any]) -> str:
    """Classify a span based on semantic conventions."""
    # Get span attributes
    attributes = span.get("attributes", {})

    # Check for Gen AI spans using multiple criteria
    if (
        LEGACY_SYSTEM in attributes
        or LEGACY_LLM in attributes
        or LEGACY_EMBEDDING in attributes
        or GEN_AI_SYSTEM in attributes
        or GEN_AI_OPERATION_NAME in attributes
        or GEN_AI_REQUEST_MODEL in attributes
        or GEN_AI_RESPONSE_MODEL in attributes
        or SpanAttributes.LLM_REQUEST_MODEL in attributes
        or SpanAttributes.LLM_RESPONSE_MODEL in attributes
        or SpanAttributes.LLM_SYSTEM in attributes
    ):
        return AgentlensSpanType.GEN_AI

    # Check for Log spans
    if LOG_SEVERITY in attributes or LOG_MESSAGE in attributes:
        return AgentlensSpanType.LOG

    # Default to Session Update span
    return AgentlensSpanType.SESSION_UPDATE


async def classify_gen_ai_span_subtype(span: Dict[str, Any]) -> str:
    """Further classify a Gen AI span into subtypes based on attributes."""
    attributes = span.get("attributes", {})

    # Check for tool usage
    if GEN_AI_TOOL_NAME in attributes or GEN_AI_TOOL_CALL_ID in attributes:
        return AgentlensGenAISpanSubtype.TOOL

    # Check for operation type
    operation_name = attributes.get(GEN_AI_OPERATION_NAME)
    if operation_name:
        if operation_name == GenAiOperationNameValues.CHAT.value:
            return AgentlensGenAISpanSubtype.CHAT
        elif operation_name == GenAiOperationNameValues.TEXT_COMPLETION.value:
            return AgentlensGenAISpanSubtype.COMPLETION
        elif operation_name == GenAiOperationNameValues.EMBEDDINGS.value:
            return AgentlensGenAISpanSubtype.EMBEDDING

    # Check for request type from LLMRequestTypeValues
    request_type = attributes.get(SpanAttributes.LLM_REQUEST_TYPE)
    if request_type:
        if request_type == LLMRequestTypeValues.CHAT.value:
            return AgentlensGenAISpanSubtype.CHAT
        elif request_type == LLMRequestTypeValues.COMPLETION.value:
            return AgentlensGenAISpanSubtype.COMPLETION
        elif request_type == LLMRequestTypeValues.EMBEDDING.value:
            return AgentlensGenAISpanSubtype.EMBEDDING

    # Check for embedding-specific attributes
    if LEGACY_EMBEDDING in attributes:
        return AgentlensGenAISpanSubtype.EMBEDDING

    # Default to general Gen AI span
    return AgentlensGenAISpanSubtype.GENERIC


async def handle_session_update_span(span: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle a session update span."""
    # Extract span data
    span_data = {
        "session_id": session_id,
        "agent_id": span.get("agent_id"),
        "trace_id": span.get("trace_id"),
        "span_id": span.get("span_id"),
        "parent_span_id": span.get("parent_span_id"),
        "name": span.get("name"),
        "kind": span.get("kind", SpanKind.INTERNAL),
        "start_time": span.get("start_time"),
        "end_time": span.get("end_time"),
        "attributes": SpanAttributeEncoder.encode(span.get("attributes", {})),
        "span_type": AgentlensSpanType.SESSION_UPDATE,
    }
    return span_data


async def handle_gen_ai_span(span: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle a Gen AI span."""
    # Get the Gen AI span subtype
    gen_ai_subtype = await classify_gen_ai_span_subtype(span)

    # Extract span data
    span_data = {
        "session_id": session_id,
        "agent_id": span.get("agent_id"),
        "trace_id": span.get("trace_id"),
        "span_id": span.get("span_id"),
        "parent_span_id": span.get("parent_span_id"),
        "name": span.get("name"),
        "kind": span.get("kind", SpanKind.CLIENT),
        "start_time": span.get("start_time"),
        "end_time": span.get("end_time"),
        "attributes": SpanAttributeEncoder.encode(span.get("attributes", {})),
        "span_type": AgentlensSpanType.GEN_AI,
        "span_subtype": gen_ai_subtype,
    }
    return span_data


async def handle_log_span(span: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle a log span."""
    # Extract span data
    span_data = {
        "session_id": session_id,
        "agent_id": span.get("agent_id"),
        "trace_id": span.get("trace_id"),
        "span_id": span.get("span_id"),
        "parent_span_id": span.get("parent_span_id"),
        "name": span.get("name"),
        "kind": span.get("kind", SpanKind.INTERNAL),
        "start_time": span.get("start_time"),
        "end_time": span.get("end_time"),
        "attributes": SpanAttributeEncoder.encode(span.get("attributes", {})),
        "span_type": AgentlensSpanType.LOG,
    }
    return span_data
