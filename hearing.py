import assemblyai as assembly
import pyaudio
import wave
import os
from absolute_path import basedir
from pathlib import Path
from dotenv import load_dotenv

class Hearing():
    def __init__(self) -> None:
        self.__format = pyaudio.paInt16
        self.__rate = 16_000
        self.__frames_per_buffer = 8192
        self.__channels = 1
        self.__wav_folder_path = "tmp/"
        self.__wav_file_path = self.__wav_folder_path + "_voice.wav"
        self.__buffers_per_second = int(self.__rate / self.__frames_per_buffer)
        Path(self.__wav_folder_path).mkdir(parents=True, exist_ok=True)
        self.__setup_inference()
        self.unmute()
    
    def listen(self, duration: float) -> bytes:
        stream = self.auditory_sense.open(
            format=self.__format,
            channels=self.__channels,
            rate=self.__rate,
            input=True,
            frames_per_buffer=self.__frames_per_buffer
        )
        print("Listening...")
        frames = []
        for _ in range(0, self.__buffers_per_second * duration):
            data = stream.read(self.__frames_per_buffer)
            frames.append(data)
        print("Time's up!")
        stream.stop_stream()
        stream.close()
        audio = b''.join(frames)
        return audio
    
    def understand(self, audio: bytes) -> str:
        self.__write_to_wav(audio, self.__wav_file_path)
        transcript = self.acoustic_sense.transcribe(self.__wav_file_path)
        return transcript.text
    
    def unmute(self) -> None:
        self.auditory_sense = pyaudio.PyAudio()

    def mute(self) -> None:
        self.auditory_sense.terminate()
    
    def __setup_inference(self) -> None:
        load_dotenv(os.path.join(basedir(), '.env'))
        assembly.settings.api_key = os.environ.get("assemblyai-api-key")
        # config = assembly.TranscriptionConfig(auto_highlights=True, punctuate=True)
        self.acoustic_sense = assembly.Transcriber()
    
    def __write_to_wav(self, audio: bytes, file_path: str) -> None:
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.__channels)
        wf.setsampwidth(self.auditory_sense.get_sample_size(self.__format))
        wf.setframerate(self.__rate)
        wf.writeframes(audio)
        wf.close()

if __name__ == "__main__":
    hearing = Hearing()
    audio = hearing.listen(10)
    hearing.mute()
    # transcript = transcriber.transcribe("https://assembly.ai/news.mp4")
    transcript = hearing.understand(audio)
    print(transcript)