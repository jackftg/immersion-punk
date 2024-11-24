
### IMPORTS
import requests  # Used for making HTTP requests

from util.file_utils import parse_json
import config as cfg
def import_silent_pygame():
    """Import pygame without displaying a welcome msg"""
    import os
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame
    return pygame
pygame = import_silent_pygame()



### CONSTANTS
CHAR_VOICE_MAPPING = parse_json(cfg.CHAR_VOICE_MAPPING_FILE)

CHUNK_SIZE = 1024  # Size of chunks to read/write at a time


### FUNCTIONS
def make_post_request(message, voice_id):
    """Make the POST request to the TTS API with headers and data, enabling streaming response"""
    
    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": cfg.ELLABS_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": message,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    if not response.ok:
        print(f"Error {response.status_code}: {response.text}")
    return response

def generate_voice_over(message, character, voice_id):
    """Generate a voice-over and save it to a file"""
    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = make_post_request(message, voice_id)
    
    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        out_path = cfg.V_VOICE_OVER_PATH if character == "V" else cfg.NPC_VOICE_OVER_PATH
        with open(out_path, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)


def play_voice_over(voice_over_fpath):
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)  # Small buffer for low latency
        pygame.mixer.music.load(voice_over_fpath)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Allows playback without blocking other operations
        print(f"Playing audio: {voice_over_fpath}")
    except Exception as e:
        print(f"Error playing audio: {e}")


def voice_message(message, character):
    """Generate a voice-over and play it"""
    voice_id = CHAR_VOICE_MAPPING[character]
    generate_voice_over(message, character, voice_id)
    voice_over_fpath = cfg.V_VOICE_OVER_PATH if character == "V" else cfg.NPC_VOICE_OVER_PATH
    play_voice_over(voice_over_fpath)
    

    






