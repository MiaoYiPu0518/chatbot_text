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

    text_widget = tk.Text(root, wrap=tk.WORD, font=("Berkeley Mono", 10))
    text_widget.pack(expand=True, fill=tk.BOTH)

    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X)

    submit_button = tk.Button(input_frame, text="Submit", command=lambda: on_submit(user_input_widget, text_widget))
    submit_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    user_input_widget = tk.Text(input_frame, wrap=tk.WORD, height=4, font=("Berkeley Mono", 10))
    user_input_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

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