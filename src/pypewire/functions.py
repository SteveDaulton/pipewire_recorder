"""Python wrapper around pipewiire CLI utilities."""
import json
import subprocess
from json import JSONDecodeError

from common import logger
from .constants import PWType, PWKey


def get_node_name(node: dict) -> str:
    """Return the Node name, or an empty string.

    Using try / except to protect against uncertainty
    in the undocumented JSON schema.
    """
    try:
        return node[PWKey.INFO][PWKey.PROPS][PWKey.NODE_NAME]
    except (KeyError, TypeError) as exc:
        logger.warning(f"Node name not found: {exc}")
        return ""


def get_pw_dump() -> list | None:
    """Return """
    try:
        json_data = subprocess.run(
            ['pw-dump'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Failed to access pw-dump: {exc}")
        return None
    try:
        return json.loads(json_data.stdout)
    except JSONDecodeError as exc:
        print(f"Invalid JSON from pw-dump: {exc}")
        return None


def get_ports(direction='input') -> list:
    pw_objects = get_pw_dump()

    if pw_objects is None:
        return []
    port_list = []
    for obj in pw_objects:
        if obj.get('type') == PWType.NODE:
            node_name = get_node_name(obj)
            if node_name:
                port_list.append(node_name)
    return port_list


def audio_sources():
    """Return a list of audio sources."""
    nodes = get_pw_dump()

    sources = []
    for node in nodes:
        # node_type = node.get("type")
        # if node_type not in node_types:
        #     node_types.add(node_type)
        #     for k, v in node.items():
        #         if isinstance(v, str) or isinstance(v, int):
        #             print(k, v)
        #         else:
        #             print(k, type(v))
        #     print()
        # Ref: https://docs.pipewire.org/page_native_protocol.html
        if node.get("type") != "PipeWire:Interface:Node":
            continue

        # Undocumented at time of writing. Reverse engineered from pw-dump.
        props = node.get("info", {}).get("props", {})
        print(props.get("media.class", "???"),
              props.get("node.name", "unknown"))
        if props.get("node.name", "unknown") in ("ardour", "Firefox"):
            print(json.dumps(node, indent=4))

        media_class = props.get("media.class", "")
        node_name = props.get("node.name", "unknown")
        description = props.get("node.description", "")

        if media_class in ("Audio/Source", "Stream/Output/Audio"):
            state = node.get("info", {}).get("state", "")
            sources.append({
                "id": node.get("id"),
                "state": state,
                "name": node_name,
                "description": description,
                "media_class": media_class,
            })
    return sources


if __name__ == '__main__':
    # print(json.dumps(get_ports(), indent=4))
    print(get_ports())
