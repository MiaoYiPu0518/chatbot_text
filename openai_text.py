import sys
import openai 
from termcolor import colored, cprint

openai.api_key = "sk-" # Input OpenAI API key here
openai.proxy = ""
GPT4 = "gpt-4"
messages = []

sys_print = lambda x : cprint(x, "yellow")

# Main function to start the AI chat
def main():
    sys_print("Welcome to the AI Chat!")
    ai_chat()

def ai_chat():
    while True:
        user_input = input("Please enter something: ")  # Ask for user input
        # Check if the user wants to quit the program
        if user_input.lower() == "quit":
            sys_print("Goodbye!\n")
            return
        
        messages.append({"role": "user", "content": user_input})
        # completion = openai.ChatCompletion.create(model=GPT4, messages=messages, stream=True)
        response = stream_response(openai.ChatCompletion.create(model=GPT4, messages=messages, stream=True))
        messages.append({"role": "assistant", "content": response})

def stream_response(completion):
    full_response = ""
    for chunk in completion:
        if not hasattr(chunk.choices[0].delta, "content"): continue 
        content = chunk.choices[0].delta.content
        sys.stdout.write(colored(content, "green"))
        full_response += content
        sys.stdout.flush()
    print()
    return full_response

# Call the main function
if __name__ == "__main__":
    main()