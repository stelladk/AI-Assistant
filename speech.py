import pyttsx3
import re

class Speech():
    def __init__(self) -> None:
        self.voice = pyttsx3.init()
        self.__current_sentence = ""
    
    def speak(self, text):
        if re.search("[\.\!\?]", text):
            self.say(self.__current_sentence)
            self.voice.runAndWait()
            self.voice.stop()
            self.__current_sentence = ""
        else:
            self.stash(text)
            
    def stash(self, text):
        self.__current_sentence += text

    def say(self, text):
        self.voice.say(text)