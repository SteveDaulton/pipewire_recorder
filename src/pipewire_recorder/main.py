import sys
import subprocess
import json
import signal

from loguru import logger

# Time stamps not required.
logger.remove()
logger.add(sys.stderr, format="<level>{level}: {message}</level>\n")



def list_audio_sources():
    result = subprocess.run(["pw-dump"], capture_output=True, text=True)
    nodes = json.loads(result.stdout)

    sources = []
    for node in nodes:
        # Ref: https://docs.pipewire.org/page_native_protocol.html
        if node.get("type") != "PipeWire:Interface:Node":
            continue

        # Undocumented at time of writing. Reverse engineered from pw-dump.
        props = node.get("info", {}).get("props", {})
        media_class = props.get("media.class", "")
        node_name = props.get("node.name", "unknown")
        description = props.get("node.description", "")

        #if media_class in ("Audio/Source", "Stream/Output/Audio"):
        if True:
            state = node.get("info", {}).get("state", "")
            sources.append({
                "id": node.get("id"),
                "state": state,
                "name": node_name,
                "description": description,
                "media_class": media_class,
            })
    return sources


record_proc = subprocess.Popen([
    "pw-record", f"--target=0", "output.wav"
])


for source in list_audio_sources():
    print(f"[{source['id']}] Name: {source['name']}  Class: {source['media_class']} ({source['state']})")


# # After launching pw-cat in background
# source_output_port = find_port_id(source_node_id, direction="output")
# pw_cat_input_port = find_pw_cat_input_port()
#
# create-link | cl    # Create a link between nodes. <node-id> <port-id> <node-id> <port-id> [<properties>]
# subprocess.run([
#     "pw-cli", "create-link",
#     str(source_output_port),
#     str(pw_cat_input_port)
# ])




# target = input("Enter source name to start recording: ")
#
# # Start recording via pw-record
# record_proc = subprocess.Popen([
#     "pw-record", f"--target={target}", "output.wav"
# ])
#
# input("Press Enter to stop recording...")
#
# # Stop recording
# record_proc.terminate()
# record_proc.wait()
#
# print("Recording saved to output.wav")


try:
    # Take care ending pw-record to avoid creating zombie nodes.
    input("Recording... Press Enter to stop\n")

    record_proc.send_signal(signal.SIGINT)
    record_proc.wait(timeout=1)
except subprocess.TimeoutExpired:
    logger.warning("pw-record shutdown failed. Forcing kill.")
    record_proc.kill()
    record_proc.wait()


