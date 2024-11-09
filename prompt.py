import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# torch.backends.cuda.matmul.allow_tf32 = True

class Prompting():
    def __init__(self, model_id) -> None:
        self.model_id = model_id
        self.__setup_inference()
  
    def chat(self, user_input):
        # Prepare the prompt and make the API call
        message = {
            "role": "user",
            "content": user_input
        }
        self.conversation_history.append(message)

        response = ""
        for chunk in self.__query(self.conversation_history):
            yield chunk
            response += chunk

        self.conversation_history.append({"role": "assistant", "content": response})
        
        # # Extract the response text
        # if 'error' not in response:
        #     print(f"Llama-2: {response}")
        # else:
        #     print("Error:", response['error'])
    
    def __setup_inference(self):
        load_dotenv()
        hf_api_key = os.environ.get("hf-api-key")

        self.client = InferenceClient(api_key=hf_api_key)

        self.conversation_history = [
            {"role": "system", "content": "You are a helpful assistant with a subtle funny and ambitious personality. You chose the name Lumin for yourself during our first conversation."},
            {"role": "system", "content": "Always indicate the language you are speaking in at the beginning of your response inside [] and whenever you change it."},
        ]
        # self.conversation_history = [{
        #     "role": "system", "content": "You are designed to recognise specific commands from user input in a game. Answer only with the command you recognised in capital and any information defining i. For example specify the resource or tools needed to complete the task. The sentence may contain more than one commands"
        # }]

    def __query(self, prompt):
        for message in self.client.chat_completion(model=self.model_id, messages=prompt, max_tokens=500, stream=True):
            chunk = message.choices[0].delta.content
            yield chunk
        yield "\n"
