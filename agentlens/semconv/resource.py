"""
Resource attribute semantic conventions for agentlens.

This module defines standard resource attributes used to identify resources in
agentlens telemetry data.
"""


class ResourceAttributes:
    """
    Resource attributes for agentlens.

    These attributes provide standard identifiers for resources being monitored
    or interacted with by agentlens.
    """

    # Project identifier - uniquely identifies an agentlens project
    PROJECT_ID = "agentlens.project.id"

    # Service attributes
    SERVICE_NAME = "service.name"
    SERVICE_VERSION = "service.version"

    # Environment attributes
    ENVIRONMENT = "agentlens.environment"
    DEPLOYMENT_ENVIRONMENT = "deployment.environment"

    # SDK attributes
    SDK_NAME = "agentlens.sdk.name"
    SDK_VERSION = "agentlens.sdk.version"

    # Host machine attributes
    HOST_MACHINE = "host.machine"
    HOST_NAME = "host.name"
    HOST_NODE = "host.node"
    HOST_OS_RELEASE = "host.os_release"
    HOST_PROCESSOR = "host.processor"
    HOST_SYSTEM = "host.system"
    HOST_VERSION = "host.version"

    # CPU attributes
    CPU_COUNT = "cpu.count"
    CPU_PERCENT = "cpu.percent"

    # Memory attributes
    MEMORY_TOTAL = "memory.total"
    MEMORY_AVAILABLE = "memory.available"
    MEMORY_USED = "memory.used"
    MEMORY_PERCENT = "memory.percent"

    # Libraries
    IMPORTED_LIBRARIES = "imported_libraries"
