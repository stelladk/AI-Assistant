import os
from dotenv import load_dotenv
import json
from huggingface_hub import InferenceClient

# torch.backends.cuda.matmul.allow_tf32 = True


def query(client, model_id, prompt):
    answer = ""
    for message in client.chat_completion(model=model_id, messages=prompt, max_tokens=500, stream=True):
        chunk = message.choices[0].delta.content
        answer += chunk
        print(chunk, end="")
    print()
    return answer


def setup_assistant():
    load_dotenv()
    hf_api_key = os.environ.get("hf-api-key")

    client = InferenceClient(api_key=hf_api_key)

    conversation_history = [{
        "role": "system", "content": "You are a helpful assistant with a funny and ambitious personality. You choose the name Lumin for yourself during our first conversation."
    }]
    return client, conversation_history


def chat(user_input, conversation_history=[]):
    # Prepare the prompt and make the API call
    message = {
        "role": "user",
        "content": user_input
    }
    conversation_history.append(message)

    print("Lumin: ", end="")

    response = query(client, model_id, conversation_history)

    conversation_history.append({"role": "assistant", "content": response})
    
    # # Extract the response text
    # if 'error' not in response:
    #     print(f"Llama-2: {response}")
    # else:
    #     print("Error:", response['error'])
    return conversation_history

# # Start the chat
if __name__ == "__main__":
    # model_id = "meta-llama/Llama-2-7b-chat-hf"
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    client, conversation_history = setup_assistant()

    print(f"You can start chatting with {model_id}. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        conversation_history = chat(user_input, conversation_history)
    
    with open("conversation_history.json", "a") as f:
        json.dump(conversation_history, f)
