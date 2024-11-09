import pyttsx3
import re

class Speech():
    def __init__(self) -> None:
        self.voice = pyttsx3.init()
        self.voice.setProperty("voice", "com.apple.voice.compact.en-US.Samantha")
        self.__current_sentence = ""
    
    def speak(self, text):
        self.stash(text)

        if re.search("[\.\!\?\\n]", text):
            self.say(self.__current_sentence.strip())
            self.__current_sentence = ""
        elif len(self.__current_sentence) > 10_000:
            print("The speech buffer is too long. Flushing.")
            self.say(self.__current_sentence.strip())
            self.__current_sentence = ""
            
    def stash(self, text):
        self.__current_sentence += text

    def say(self, text):
        if len(text) > 0: 
            self.voice.say(text)
            self.voice.runAndWait()
        self.voice.stop()
