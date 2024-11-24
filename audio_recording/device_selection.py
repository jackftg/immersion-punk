
### IMPORTS
import sounddevice as sd
import config as cfg


### FUNCTIONS
def auto_select_microphone():
    """
    Set the config.MICROPHONE_DEVICE_ID based on the config.MICROPHONE_NAME.

    If the config.MICROPHONE_NAME is None or no matching device is found,
    prompt the user to select a microphone by index.
    """
    if cfg.MICROPHONE_NAME is None:
        print("\nNo microphone name set in config. Prompting for manual selection...")
        select_microphone_manually()
        return

    # Find the device ID based on the name in the config
    try:
        devices = sd.query_devices()
    except Exception as e:
        raise RuntimeError("Failed to query audio devices. Ensure sounddevice is installed and working.") from e

    matching_devices = [index for index, device in enumerate(devices)
                        if cfg.MICROPHONE_NAME.lower() in device['name'].lower() and device['max_input_channels'] > 0]

    if matching_devices:
        cfg.MICROPHONE_DEVICE_ID = matching_devices[0]  # Use the first match
        print(f"\nMicrophone '{cfg.MICROPHONE_NAME}' found at index {cfg.MICROPHONE_DEVICE_ID} "
              f"with full name {devices[cfg.MICROPHONE_DEVICE_ID]['name']}.")
    else:
        print(f"\nMicrophone '{cfg.MICROPHONE_NAME}' not found.")
        select_microphone_manually()

def list_microphones():
    """List all available microphones."""
    print("\nAvailable microphones:")
    try:
        devices = sd.query_devices()
        if not devices:
            raise ValueError("No microphones found!")
    except Exception as e:
        raise RuntimeError("Failed to query audio devices.") from e

    for index, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"Index {index}: {device['name']} (Input Channels: {device['max_input_channels']})")


def select_microphone_manually():
    """Prompt the user to select a microphone by index or quit."""
    list_microphones()

    while True:
        try:
            print("\nPlease manually select the microphone you want to use for voice input.")
            print("Alternatively, provide a valid microphone name in config.py and restart the script.")
            print("Type 'q' or 'quit' to exit the program.\n")

            user_input = input("Type in its index and press ENTER: ").strip().lower()

            # Check if user wants to quit
            if user_input in ('q', 'quit'):
                print("Exiting program. No microphone selected.")
                exit()  # Terminate the program

            # Validate if input is a valid integer
            selected_device_index = int(user_input)

            # Validate the selected index
            devices = sd.query_devices()
            if 0 <= selected_device_index < len(devices) and devices[selected_device_index]['max_input_channels'] > 0:
                cfg.MICROPHONE_DEVICE_ID = selected_device_index
                print(f"Selected microphone: {selected_device_index} - {devices[selected_device_index]['name']}")
                return
            else:
                print(f"Invalid index or device has no input channels. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid integer index, or type 'q' to quit.")
        except Exception as e:
            print(f"An error occurred: {e}")
