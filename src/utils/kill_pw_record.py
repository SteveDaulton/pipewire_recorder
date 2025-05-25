"""kill_pw_record

A utility to clean up any pw-record processes that were
not shut down cleanly.
"""

import subprocess
import os
import signal

def get_pw_record_pids():
    try:
        # Use ps and grep to find pw-record processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        pids = []

        for line in lines:
            if 'pw-record' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) > 1:
                    pid = int(parts[1])
                    pids.append(pid)
        return pids

    except Exception as e:
        print(f"Error retrieving process list: {e}")
        return []

def stop_pw_record_processes(pids):
    for pid in pids:
        try:
            print(f"Sending SIGINT to pw-record process PID {pid}")
            os.kill(pid, signal.SIGINT)
        except ProcessLookupError:
            print(f"Process {pid} no longer exists.")
        except PermissionError:
            print(f"Permission denied when trying to signal PID {pid}.")
        except Exception as e:
            print(f"Error stopping PID {pid}: {e}")

def main():
    pids = get_pw_record_pids()
    if not pids:
        print("No pw-record processes found.")
        return
    print(pids)
    stop_pw_record_processes(pids)

if __name__ == "__main__":
    main()
