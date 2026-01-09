#!/usr/bin/env python3
import sys
import json
import struct
import os
import subprocess
import threading
import time

def send_message(msg):
    try:
        content = json.dumps(msg, separators=(',', ':'))
        # Write length (4 bytes, native byte order)
        # Firefox expects native byte order for length
        sys.stdout.buffer.write(struct.pack('@I', len(content)))
        sys.stdout.buffer.write(content.encode('utf-8'))
        sys.stdout.buffer.flush()
    except (BrokenPipeError, IOError):
        sys.exit(0)

def read_scheme(path):
    try:
        # Retry logic in case the file is being written to
        for _ in range(3):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                time.sleep(0.1)
                continue
            except FileNotFoundError:
                return None
        return None
    except Exception:
        return None

def read_stdin():
    """Read from stdin to detect when the browser closes the connection."""
    while True:
        try:
            # Read message length (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if len(raw_length) == 0:
                # EOF - Browser closed the pipe
                os._exit(0)
            length = struct.unpack('@I', raw_length)[0]
            # Read the message (we don't actually use it, just consume it)
            if length > 0:
                sys.stdin.buffer.read(length)
        except Exception:
            os._exit(0)

def main():
    scheme_dir = os.path.expanduser("~/.local/state/caelestia")
    scheme_path = os.path.join(scheme_dir, "scheme.json")

    # Start stdin reader thread
    # This is CRITICAL: it keeps the buffer empty and detects browser exit
    thread = threading.Thread(target=read_stdin, daemon=True)
    thread.start()

    # Initial send
    scheme = read_scheme(scheme_path)
    if scheme:
        send_message(scheme)

    # Watch for changes
    try:
        if not os.path.exists(scheme_dir):
            os.makedirs(scheme_dir, exist_ok=True)

        # Monitor the directory
        process = subprocess.Popen(
            ['inotifywait', '-q', '-e', 'close_write,moved_to,create', '-m', scheme_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        while True:
            line = process.stdout.readline()
            if not line:
                break
            try:
                decoded = line.decode('utf-8', errors='ignore').strip()
                parts = decoded.split()
                # inotifywait -m output: directory events filename
                # e.g., /path/to/dir/ CLOSE_WRITE scheme.json
                # OR just filename if -q is used sometimes, but let's be safe
                if len(parts) >= 1 and parts[-1] == 'scheme.json':
                    # Add a small delay to ensure write is complete
                    time.sleep(0.05)
                    scheme = read_scheme(scheme_path)
                    if scheme:
                        send_message(scheme)
            except Exception:
                pass
    except FileNotFoundError:
        # inotify-tools not installed
        pass
    except Exception:
        pass

if __name__ == "__main__":
    main()