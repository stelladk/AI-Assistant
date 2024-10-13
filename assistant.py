from prompt import Prompting

import json

class AIAssistant(Prompting):
    def __init__(self, name="Lumin") -> None:
        model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        super().__init__(model_id)
        self.name = name


# Start the chat
if __name__ == "__main__":

    assistant = AIAssistant()

    print(f"You can start chatting with {assistant.model_id}. Type 'exit' to quit.\n")

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
