import os
import time

from llm.llm import process_message


def watch_trigger_file(chat_session, file_name):
    """
    Watch for the user having submitted a message.

    The submitted is saved to a file for communication.
    """
    print(f"Watching for file: {file_name}")
    last_mtime = 0
    while True:
        if os.path.exists(file_name):  # Check if the file exists
            mtime = os.path.getmtime(file_name)  # Get the file's last modified time
            if mtime > last_mtime:  # If the file has been modified
                last_mtime = mtime
                with open(file_name, 'r') as f:  # Open the file
                    message = f.read().strip()  # Read and strip the content
                    process_message(chat_session, message)  # Process the message
                os.remove(file_name)  # Delete the file after processing
        time.sleep(0.1)  # Sleep to reduce CPU usage
