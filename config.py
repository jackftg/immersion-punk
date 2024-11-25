
### IMPORTS
import os


### CONFIG & CONSTANTS
## API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELLABS_API_KEY = os.getenv("11LABS_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set as environment variable")
if not ELLABS_API_KEY:
    raise ValueError("11LABS_API_KEY must be set as environment variable")


## Voicing
VOICE_V = True
VOICE_NPCS = True

VOICE_DELAY = 0.5  # in seconds

## Config for Voice Input
ENABLE_VOICE_INPUT = False
# Specify the name of your microphone
# You don't need to specify the full name
MICROPHONE_NAME = "RODE"
MICROPHONE_DEVICE_ID = None  # DO NOT manually set this


## File paths
# Mappings
CHAR_VOICE_MAPPING_FILE = "char_voice_mapping.json"
CHAR_BACKGROUND_FILE = "char_background.json"

# Voice over results
V_VOICE_OVER_PATH = "results/v_voice_over.mp3"
NPC_VOICE_OVER_PATH = "results/npc_voice_over.mp3"

# Message files for communicating between python and lua
USER_MESSAGE_FPATH = "vs_message.txt"
RESPONSE_FPATH = "response.txt"  # File to store the llm's response

# Recordings
USER_RECORDING_FPATH = "results/user_recording.wav"

# Model paths
VOSK_MODEL_PATH = "models/vosk-model-en-us-0.22"


