import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav


# Load Whisper model (can be "tiny", "base", "small", "medium", "large")
model = whisper.load_model("base")

# Audio recording settings
DURATION = 5  # seconds
SAMPLE_RATE = 16000  # Whisper expects 16000 Hz

def record_audio(duration, sample_rate):
    print("🎙️ Speak now...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    print("✅ Recording finished.")
    return audio.flatten()

def save_temp_wav(audio_data, sample_rate):
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav.write(tmpfile.name, sample_rate, (audio_data * 32767).astype(np.int16))
    return tmpfile.name

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    audio_data = record_audio(DURATION, SAMPLE_RATE)
    temp_audio_path = save_temp_wav(audio_data, SAMPLE_RATE)
    transcription = transcribe(temp_audio_path)
    print("📝 Transcription:", transcription)