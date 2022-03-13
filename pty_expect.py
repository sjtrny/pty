import sys
import os
import pty
import subprocess
import shlex
import selectors
import multiprocessing as mp


def run(cmd, input_lines=[]):
    """Run an interactive given command with input and capture all IO.

    Parameters
    ----------
    cmd: str
         The command to run
    input_lines: list
         List of str with each line of text to be entered into the running cmd
    """
    q = mp.Queue()

    try:
        (child_pid, fd) = pty.fork()
    except OSError as e:
        print(str(e))

    if child_pid == 0:
        sys.stdout.flush()
        try:
            subprocess.run(shlex.split(cmd))
        except subprocess.SubprocessError:
            print("Couldn't spawn subprocess...")

        f = open(os.devnull, "w")
        sys.stdout = f
        q.put("FINISHED")
        return
    else:
        data = b""

        sel = selectors.DefaultSelector()
        sel.register(fd, selectors.EVENT_READ)

        line_pos = 0

        while True:

            # Block until new event
            sel.select()

            # Read all available data
            while True:
                events = sel.select(-1)

                # No more events, stop reading
                if len(events) == 0:
                    break

                read_data = os.read(fd, 1024)
                if read_data:
                    data += read_data

            # Write if we have something to write
            # otherwise skip to final read only mode
            if line_pos <= len(input_lines) - 1:
                os.write(fd, (input_lines[line_pos] + "\n").encode("utf-8"))
                line_pos += 1
            else:
                break

        # Wait for child process to signal end
        q.get(block=True)

        while True:
            events = sel.select(-1)

            # No more events, stop reading
            if len(events) == 0:
                break

            read_data = os.read(fd, 1024)
            if read_data:
                data += read_data

        return data.decode("utf-8")
