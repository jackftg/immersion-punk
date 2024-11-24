
### IMPORTS
import sounddevice as sd
import soundfile as sf
import queue
import config as cfg
from audio_recording import transcription


### FUNCTIONS
def record_audio(stop_event, transcribe=False):
    """Record audio and save to a .wav file as mono PCM."""
    q = queue.Queue()
    with sf.SoundFile(cfg.USER_RECORDING_FPATH, mode='w', samplerate=16000,
                      channels=1, subtype='PCM_16') as file:  # Ensure mono (channels=1) and PCM 16-bit
        with sd.InputStream(samplerate=16000, channels=1, dtype='int16',
                            device=cfg.MICROPHONE_DEVICE_ID,
                            callback=lambda indata, frames, time, status: q.put(indata.copy())):
            while not stop_event.is_set():
                while not q.empty():
                    file.write(q.get())

    if transcribe:
        transcription_result = transcription.transcribe_user_audio()
        # TODO Do sth with result


