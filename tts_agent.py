# voice_agent/tts_agent.py

from TTS.api import TTS
import os
import soundfile as sf


class VoiceAgent:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        print(f"Loading TTS model: {model_name}")
        self.tts = TTS(model_name)

    def speak(self, text: str, output_path="output.wav") -> str:
        # Generate speech and save to file
        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path


# Example usage
if __name__ == "__main__":
    voice = VoiceAgent()
    out_file = voice.speak("Good morning. Your Asia tech exposure is at 22%, with TSMC beating earnings.")
    print(f"✅ Audio saved to: {out_file}")
    os.system("aplay ./output.wav")
