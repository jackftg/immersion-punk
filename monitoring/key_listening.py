
### IMPORTS
from pynput import keyboard
from audio_recording.recording import record_audio
import threading
from functools import partial


### GLOBAL VARIABLES
is_recording = False  # Flag to indicate if recording is active
record_thread = None
stop_event = threading.Event()


### FUNCTIONS
def toggle_record_on_press(key, transcribe=False):
    """Callback for key press to toggle recording."""
    global is_recording, record_thread, stop_event
    try:
        if key == keyboard.Key.shift_r:
            if not is_recording:
                # Start recording
                is_recording = True
                stop_event.clear()
                record_thread = threading.Thread(target=record_audio, args=(stop_event, transcribe))
                record_thread.start()
                print("Recording started...")
            else:
                # Stop recording
                is_recording = False
                print("Recording stopped.")
                stop_event.set()
                if record_thread:
                    record_thread.join()  # Wait for the thread to finish cleanly
    except AttributeError:
        pass


def start_recording_hotkey_listener():
    """Start hotkey listener to toggle audio recording."""
    print("\nPress the right shift key to start/stop recording your voice.")
    with keyboard.Listener(on_press=partial(toggle_record_on_press, transcribe=True)) as listener:
        listener.join()
