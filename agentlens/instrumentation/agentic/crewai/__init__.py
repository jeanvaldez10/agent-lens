"""OpenTelemetry CrewAI instrumentation"""

from agentlens.instrumentation.agentic.crewai.version import __version__
from agentlens.instrumentation.agentic.crewai.instrumentation import CrewaiInstrumentor

__all__ = ["CrewaiInstrumentor", "__version__"]
