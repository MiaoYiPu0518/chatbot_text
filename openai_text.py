import sys
import os
import openai 
from termcolor import colored, cprint

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.proxy = os.getenv('OPENAI_PROXY') 
GPT4 = "gpt-4"
messages = [] # chat history 
sys_print = lambda x : cprint(x, "yellow") # Used to print system message

def main():
    sys_print("Welcome to the AI Chat!")
    ai_chat()

def ai_chat():
    while True:
        user_input = input("Please enter message: ")  # Ask for user input
        # if enter "quit" then quit the program
        if user_input.lower() == "quit":
            sys_print("Goodbye!\n")
            return
        
        messages.append({"role": "user", "content": user_input})
        response = stream_response(openai.ChatCompletion.create(model=GPT4, messages=messages, stream=True))
        messages.append({"role": "assistant", "content": response})

def stream_response(completion):
    full_response = ""
    for chunk in completion:
        # Skip the chunk if it doesn't have "content" attribute
        if not hasattr(chunk.choices[0].delta, "content"): continue
        
        content = chunk.choices[0].delta.content
        sys.stdout.write(colored(content, "green"))
        full_response += content
        sys.stdout.flush()
    
    print() # formatting 
    return full_response

if __name__ == "__main__":
    main()