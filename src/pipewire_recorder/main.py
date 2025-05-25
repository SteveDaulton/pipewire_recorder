import subprocess
import signal

from common import logger
from pypewire import get_ports


record_proc = subprocess.Popen([
    "pw-record", "--target=0", "output.wav"
])

ports = get_ports()
print()
assert ports is not None
for source in ports:
    print(f"[{source['id']}] Name: {source.get('name', '???')}  "
          f"Class: {source.get('media_class', '???')} ({source.get('state')})")


# # After launching pw-cat in background
# source_output_port = find_port_id(source_node_id, direction="output")
# pw_cat_input_port = find_pw_cat_input_port()
#
# create-link | cl    # Create a link between nodes.
# <node-id> <port-id> <node-id> <port-id> [<properties>]
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
