
### IMPORTS
import wave
import sys
import config as cfg

from vosk import Model, KaldiRecognizer, SetLogLevel


### CONFIG & GLOBALS
# You can set log level to -1 to disable debug messages
SetLogLevel(0)
model = None


### FUNCTIONS
def init_model():
    global model
    print("\nLoading Vosk model for audio transcription..")
    model = Model(model_path=cfg.VOSK_MODEL_PATH)
    print("Vosk model loaded.")

def transcribe_user_audio():
    global model
    # Load model if not already
    if model is None:
        init_model()

    # Load audio file
    wf = wave.open(cfg.USER_RECORDING_FPATH, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    # Transcription setup
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    # Transcribe
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # print(rec.Result())
            pass
        else:
            # print(rec.PartialResult())
            pass

    final_result = rec.FinalResult()
    print("\nTranscription result:")
    print(final_result)
    return final_result






