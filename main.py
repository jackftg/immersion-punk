
### IMPORTS
import config as cfg
from audio_recording import transcription, device_selection

from llm import llm
from monitoring import key_listening
from monitoring import file_watching
from util import file_utils


### MAIN
if __name__ == "__main__":

    ## Parse relevant files
    char_backgrounds = file_utils.parse_json(cfg.CHAR_BACKGROUND_FILE)

    ## LLM Setup
    model = llm.configure_model()
    chat_session = llm.create_chat_session(model, char_backgrounds["PanamPalmer"])

    ## Voice Input Setup
    if cfg.ENABLE_VOICE_INPUT:
        device_selection.auto_select_microphone()
        transcription.init_model()
        key_listening.start_recording_hotkey_listener()

    ## Listen for user submitted messages
    file_watching.watch_trigger_file(chat_session, cfg.USER_MESSAGE_FPATH)
