import os
from dotenv import load_dotenv
import json
from huggingface_hub import InferenceClient

# torch.backends.cuda.matmul.allow_tf32 = True

class Prompting():
    def __init__(self, model_id) -> None:
        self.model_id = model_id
        self.setup_inference()

    @property
    def conversation_history(self):
        return self.__conversation_history
  
    def chat(self, user_input):
        # Prepare the prompt and make the API call
        message = {
            "role": "user",
            "content": user_input
        }
        self.conversation_history.append(message)

        response = self.__query(self.conversation_history)

        self.conversation_history.append({"role": "assistant", "content": response})
        
        # # Extract the response text
        # if 'error' not in response:
        #     print(f"Llama-2: {response}")
        # else:
        #     print("Error:", response['error'])
    
    def setup_inference(self):
        load_dotenv()
        hf_api_key = os.environ.get("hf-api-key")

        self.client = InferenceClient(api_key=hf_api_key)

        self.__conversation_history = [{
            "role": "system", "content": "You are a helpful assistant with a funny and ambitious personality. You choose the name Lumin for yourself during our first conversation."
        }]

    def __query(self, prompt):
        answer = ""
        for message in self.client.chat_completion(model=self.model_id, messages=prompt, max_tokens=500, stream=True):
            chunk = message.choices[0].delta.content
            answer += chunk
            print(chunk, end="")
        print()
        return answer


# # Start the chat
if __name__ == "__main__":
    # model_id = "meta-llama/Llama-2-7b-chat-hf"
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    prompt = Prompting(model_id)

    print(f"You can start chatting with {model_id}. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        print(f"Lumin: ", end="")

        prompt.chat(user_input)
    
    with open("conversation_history.json", "a") as f:
        json.dump(prompt.conversation_history, f)
