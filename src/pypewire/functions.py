"""Python wrapper around pipewiire CLI utilities."""
import json
import subprocess
from json import JSONDecodeError

from pypewire.constants import PWType


def get_ports(direction='input'):
    try:
        json_data = subprocess.run(
            ['pw-dump'],
            capture_output=True, text=True, check=False)
    except subprocess.CalledProcessError as exc:
        print(f"Failed to access pw-dump: {exc}")
        return None
    try:
        pw_objects = json.loads(json_data.stdout)
    except JSONDecodeError as exc:
        print(f"Invalid JSON from pw-dump: {exc}")
        return None
    port_list = []
    for obj in pw_objects:
        if obj.get('type') == PWType.NODE:
            port_list.append(obj)
    return port_list

def audio_sources():
    """Return a list of audio sources."""
    result = subprocess.run(["pw-dump"], capture_output=True, text=True)
    nodes = json.loads(result.stdout)

    sources = []
    node_types = set()
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
        print(props.get("media.class", "???"), props.get("node.name", "unknown"))
        if props.get("node.name", "unknown") in ("ardour", "Firefox"):
            print(json.dumps(node, indent=4))

        media_class = props.get("media.class", "")
        node_name = props.get("node.name", "unknown")
        description = props.get("node.description", "")

        if media_class in ("Audio/Source", "Stream/Output/Audio"):
        #if True:
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
    get_ports()