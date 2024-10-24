from prompt import Prompting
from speech import Speech
from hearing import Hearing
import json


class AIAssistant(Prompting, Speech, Hearing):
    def __init__(self, name="Lumin") -> None:
        model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        Prompting.__init__(self, model_id)
        Speech.__init__(self)
        Hearing.__init__(self)
        self.name = name
    
    def chat(self, user_input):
        for chunk in super().chat(user_input):
            yield chunk
            self.speak(chunk)
    
    def mute(self):
        super().mute()
        self.voice.stop()


# Start the chat
if __name__ == "__main__":

    assistant = AIAssistant()

    print(f"You can start chatting with {assistant.model_id}. Type 'exit' to quit.\n")

    # print(f"{assistant.name}: ", end="")
    # for chunk in assistant.chat(""):
    #     print(chunk, end="")

    # TODO: save all answers immidiately

    while True:
        try:
            input("Press enter to start speaking")
            user_audio = assistant.listen(15)
            user_input = assistant.understand(user_audio)
        except Exception as error:
            print(error)
            user_input = input("You: ")
        
        print(f"You: {user_input}")

        if "exit" in user_input.lower():
            print("Goodbye!")
            assistant.mute()
            break

        print(f"{assistant.name}: ", end="")

        for chunk in assistant.chat(user_input):
            print(chunk, end="")
    
    with open("conversation_history.json", "a") as f:
        json.dump(assistant.conversation_history, f)
