import sys
import os
import openai 
import tkinter as tk
import threading
from termcolor import colored, cprint

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.proxy = os.getenv('OPENAI_PROXY') 
GPT4 = "gpt-4"
messages = [] # chat history 
sys_print = lambda x : cprint(x, "yellow") # Used to print system message

def main():
    sys_print("Welcome to the AI Chat!")
    create_gui()

def create_gui():
    root = tk.Tk()
    root.title("AI Chat")

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    user_input_widget = tk.Text(root, wrap=tk.WORD, height=4)
    user_input_widget.pack(fill=tk.X)

    submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(user_input_widget, text_widget))
    submit_button.pack()
    root.mainloop()

def stream_response(completion, text_widget):
    full_response = ""
    for chunk in completion:
        # Skip the chunk if it doesn't have "content" attribute
        if not hasattr(chunk.choices[0].delta, "content"): continue

        content = chunk.choices[0].delta.content
        text_widget.insert(tk.END, content)
        text_widget.see(tk.END)
        full_response += content

    messages.append({"role": "assistant", "content": full_response})
    print(messages)

def on_submit(user_input_widget, text_widget):
    user_input = user_input_widget.get("1.0", tk.END).strip()
    user_input_widget.delete("1.0", tk.END)

    if user_input.lower() == "quit":
        sys.exit()

    messages.append({"role": "user", "content": user_input})
    text_widget.insert(tk.END, f"\nUser: {user_input}\n")
    text_widget.see(tk.END)

    response_thread = threading.Thread(target=stream_response, args=(openai.ChatCompletion.create(model=GPT4, messages=messages, stream=True, temperature=0.7), text_widget))
    response_thread.start()
    

if __name__ == "__main__":
    main()