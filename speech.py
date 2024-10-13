import pyttsx3
import re

class Speech():
    def __init__(self) -> None:
        self.voice = pyttsx3.init()
        self.voice.setProperty("voice", "com.apple.voice.compact.en-US.Samantha")
        self.__current_sentence = ""
    
    def speak(self, text):
        if re.search("[\.\!\?]", text):
            self.say(self.__current_sentence)
            self.__current_sentence = ""
        else:
            self.stash(text)
            
    def stash(self, text):
        self.__current_sentence += text

    def say(self, text):
        self.voice.say(text)
        self.voice.runAndWait()
        self.voice.stop()
