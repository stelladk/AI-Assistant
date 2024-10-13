from prompt import Prompting
from speech import Speech

import json

class AIAssistant(Prompting, Speech):
    def __init__(self, name="Lumin") -> None:
        model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        Prompting.__init__(self, model_id)
        Speech.__init__(self)
        self.name = name
    
    def chat(self, user_input):
        for chunk in super().chat(user_input):
            yield chunk
            self.speak(chunk)


# Start the chat
if __name__ == "__main__":

    assistant = AIAssistant()

    print(f"You can start chatting with {assistant.model_id}. Type 'exit' to quit.\n")

    print(f"{assistant.name}: ", end="")
    for chunk in assistant.chat(""):
        print(chunk, end="")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        print(f"{assistant.name}: ", end="")

        for chunk in assistant.chat(user_input):
            print(chunk, end="")
    
    with open("conversation_history.json", "a") as f:
        json.dump(assistant.conversation_history, f)
