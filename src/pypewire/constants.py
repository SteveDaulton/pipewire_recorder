"""Constants and Enumerations.

Reverse engineered from pw_dump due to lack of documentation.
"""

from enum import StrEnum


class PWKey:
    """Common object keys."""
    # Top level.
    ID = 'id'
    TYPE = 'type'
    VERSION = 'version'
    PERMISSIONS = 'permissions'
    INFO = 'info'
    PROPS = 'props'
    METADATA = 'metadata'
    # Other known fields.
    DIRECTION = 'direction'
    PARAMS = 'params'
    NODE_NAME = 'node.name'


class PWType(StrEnum):
    """Known PipeWire interface types as observed in pw-dump outputs."""
    CLIENT = 'PipeWire:Interface:Client'
    CORE = 'PipeWire:Interface:Core'
    DEVICE = 'PipeWire:Interface:Device'
    FACTORY = 'PipeWire:Interface:Factory'
    LINK = 'PipeWire:Interface:Link'
    METADATA = 'PipeWire:Interface:Metadata'
    MODULE = 'PipeWire:Interface:Module'
    NODE = 'PipeWire:Interface:Node'
    PORT = 'PipeWire:Interface:Port'
    PROFILER = 'PipeWire:Interface:Profiler'
    CLIENT_NODE = 'PipeWire:Interface:ClientNode'
    CLIENT_DEVICE = 'PipeWire:Interface:ClientDevice'
    CLIENT_ENDPOINT = 'PipeWire:Interface:ClientEndpoint'
    CLIENT_SESSION = 'PipeWire:Interface:ClientSession'
    SESSION = 'PipeWire:Interface:Session'
    ENDPOINT = 'PipeWire:Interface:Endpoint'
    ENDPOINT_STREAM = 'PipeWire:Interface:EndpointStream'
    ENDPOINT_LINK = 'PipeWire:Interface:EndpointLink'
