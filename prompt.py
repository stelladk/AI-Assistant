import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# torch.backends.cuda.matmul.allow_tf32 = True

class Prompting():
    def __init__(self, model_id) -> None:
        self.model_id = model_id
        self.setup_inference()
  
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
    
    def setup_inference(self):
        load_dotenv()
        hf_api_key = os.environ.get("hf-api-key")

        self.client = InferenceClient(api_key=hf_api_key)

        self.conversation_history = [{
            "role": "system", "content": "You are a helpful assistant with a funny and ambitious personality. You choose the name Lumin for yourself during our first conversation."
        }]

    def __query(self, prompt):
        for message in self.client.chat_completion(model=self.model_id, messages=prompt, max_tokens=500, stream=True):
            chunk = message.choices[0].delta.content
            yield chunk
        yield "\n"
